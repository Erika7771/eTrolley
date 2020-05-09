/*The  code below creates a connection to the websocket and listen on 
 * the sensors channels. Each time a new data is sent, the corresponding 
 * graph is updated.*/

$(function () {
   
    /* Define styles for each graph*/
    var ticksStyle = {
        fontColor: '#495057'
    }

    var optStyle = {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                gridLines: {
                    display: true
                },
                ticks: $.extend({
                    beginAtZero: true,
                    suggestedMax: 1000
                }, ticksStyle)
            }],
            xAxes: [{
                display: false,
                scaleLabel: {
                    display: false
                },
                ticks: ticksStyle
            }]
        }
    }
    
    var optStyle2 = JSON.parse(JSON.stringify(optStyle));
    var optStyle3 = JSON.parse(JSON.stringify(optStyle));
    var optStyle4 =JSON.parse(JSON.stringify(optStyle));
    optStyle2['scales']['yAxes'][0]['ticks']['suggestedMax'] = 3;
    optStyle3['scales']['yAxes'][0]['ticks']['suggestedMax'] = 300;
    optStyle4['scales']['yAxes'][0]['ticks']['suggestedMax'] = 10000;

    
    var optStyle5 = {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                id: 'A',
                position: 'left',           
                gridLines: {
                    display: true
                },
                ticks: $.extend({
                    beginAtZero: true,
                    suggestedMax : 256
                }, ticksStyle)
                },
                {
                    id: 'B',
                    position: 'right',
                    display: false,  //set to true to see it on the graph         
                    gridLines: {
                        display: true 
                    },
                    ticks: $.extend({
                        beginAtZero: true,
                        suggestedMax : 50000
                    }, ticksStyle)
                }],
            xAxes: [{
                display: false,
                scaleLabel: {
                    display: false
                },
                ticks: ticksStyle
            }]
        }
    } 
    
    var namespace = '/sensors';
    var socket = io(namespace);
    socket.close();    

    var zero = 0;
    var readyToRequest = true;
    
    /* Update the graph with the new data */
    function drawGraph(graph, newData, checkReady) {
        var i;
        var j;
        var tooLong = graph.data.datasets[0].data.length > 300;

        for (i = 0; i < newData.length; i++) {
            graph.data.labels.push(zero);
            if (tooLong) {
                graph.data.labels.splice(0, 1);
            }
            for (j = 0; j < graph.data.datasets.length; j++) {
                if (tooLong) {
                    graph.data.datasets[j].data.splice(0, 1);
                }
                graph.data.datasets[j].data.push(newData[i][j]);
            }
            zero++;
        }
        graph.update();
    }

   /* Set some charts representation options and define the basic
    * structure of each graph.*/
    Chart.defaults.global.elements.line.fill = false;
    Chart.defaults.global.elements.line.borderWidth = 1;
    Chart.defaults.global.elements.line.tension = 0;
    Chart.defaults.global.elements.point.radius = 0;
    Chart.defaults.global.animation.duration = 0;
    Chart.defaults.global.legend.display = false;
    Chart.defaults.global.tooltips.enable = false;

    var $IMU12 = $('#IMU12');
    var IMU12 = new Chart($IMU12, {
        type: 'line',
        data: {
            datasets: [
                {
                    data: [],
                    borderColor: '#6BC1FF'
                },
                {
                    data: [],
                    borderColor: '#52FF89'
                },
                {
                    data: [],
                    borderColor: '#FF7A78'
                }]
        },
        options: optStyle
    })


    var $IMUangVel = $('#IMUangVel')
    var IMUangVel = new Chart($IMUangVel, {
        type: 'line',
        data: {
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            },
                {
                    data: [],
                    borderColor: '#52FF89'
                },
                {
                    data: [],
                    borderColor: '#FF7A78'
                }]
        },
        options: optStyle
    })

    var $RazorIMU = $('#RazorIMU');
    var RazorIMU = new Chart($RazorIMU, {
        type: 'line',
        data: {
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            },
                {
                    data: [],
                    borderColor: '#52FF89'
                },
                {
                    data: [],
                    borderColor: '#FF7A78'
                }]
        },
        
        options: optStyle2
        
    })

    var $RazorIMUvel = $('#RazorIMUvel')
    var RazorIMUvel = new Chart($RazorIMUvel, {
        type: 'line',
        data: {
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            },
                {
                    data: [],
                    borderColor: '#52FF89'
                },
                {
                    data: [],
                    borderColor: '#FF7A78'
                }]
        },
        options: optStyle3
    })

    var $LoadCell = $('#LoadCell')
    var LoadCell = new Chart($LoadCell, {
        type: 'line',
        data: {
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            }]
        },
        options: optStyle4
    })

    var $CAN = $('#CAN')
    var CAN = new Chart($CAN, {
        type: 'line',
        data: {
            datasets: [{
                yAxisID: 'A',
                data: [],
                borderColor: '#6BC1FF'
            },
                {   
                    yAxisID: 'A',
                    data: [],
                    borderColor: '#52FF89'
                },
                {   
                    yAxisID: 'A',
                    data: [],
                    borderColor: '#FF7A78'
                }]
        },
        options: optStyle5
    })
    /* This event fires when the user selects the sensors from the dropdowns.
     * If the dropdown is for the readings, renderSelectedGraphs is called
     * and only the selected graphs are shown.
     * If the dropdown is for the recordings, the links necessary to then 
     * download the files are set up */
    $('.selectpicker').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
        var latest_value = $(this).children('option').eq(clickedIndex).val();
        var latest_selection = isSelected;
        var selectedValues = $(this).val();
        var allIsSelected = selectedValues.includes("all");

        if(latest_value=='all' && latest_selection){
            $(this).selectpicker('selectAll');
        }else if(latest_value=='all' && latest_selection===false){
            $(this).selectpicker('deselectAll');
        }else if(latest_value=='all' && !latest_selection){ //evita di fare due volte il render
            return;
        }

        if(latest_value!='all' && allIsSelected){
            var selectedValues = selectedValues.filter(function(e) { return e !== 'all' })
            $(this).selectpicker('val', selectedValues);
            $(this).selectpicker('refresh');
        }

        if($(this).data("type")=='reading'){
            renderSelectedGraphs($(this).val());
        }
    
        if($(this).data("type")=='recording'){            
            var sensorsToken = $('#selectRecordings').val().join(';');
            $("#downloadFiles").attr("href","/recordings/last_recording?data="+sensorsToken+"&rnd="+Math.random());
            $("#downloadUnifile").attr("href","/recordings/unifile");
        }

    });
    /*This function shows or hides the graphs depending on which are selected. */
    function renderSelectedGraphs(graphs){
        var renderer = this;
        var howMany = graphs.length;
        $(".card.sensor").parents(".sensorColumn").hide();
        $.each(graphs, function( index, sensorName) {
            var $el = $(".card.sensor[data-sensor='"+sensorName+"']").parents(".sensorColumn");
            $el.show();
            if(howMany < 2){
                $el.removeClass("col-lg-6").addClass("col-md-12");
            }else{
                $el.addClass("col-lg-6").removeClass("col-md-12");
            }
        });
    }
   
    $("#rec").hide();      
    var isRecording = false;
    
    /*This event fires when the "Start" buttons are clicked and changes
     *their appearance (ex green Start -> red Stop) and enables/disables 
     *the others buttons (ex. to avoid recording before connecting)
     * Depending on wich button is pressed and its previous state, 
       stopReading, Recording or startReading is called.*/
    $(".readSensors, .recordSensors").click(function(){
        
        var reading = $(this).hasClass("readSensors");
        var idPicker = reading?'#selectReadings':"#selectRecordings";        
        
        
        if ($(this).hasClass('running')) {

            if(reading){
                stopReading();
                $(".recordSensors").children('span').html('Start');
                $("#rec").hide(); 
                $(".recordSensors").prop('disabled', true);
            }else{                
                Recording('stop');      
                    $("#rec").hide();
                    $(".readSensors").prop('disabled', false);  
                    $(".dwldButtons").removeClass('disabled');            
            }
            
            $(idPicker).prop('disabled', false);
            $(idPicker).selectpicker('refresh');
            $(this).removeClass('running');
            $(this).children('i').removeClass('text-danger').removeClass('fa-stop');
            $(this).children('i').addClass('text-success').addClass('fa-play');
            $(this).children('span').html('Start');

        } else {

            if(reading){ 
                startReading(); 
                        
            }else{
                    $("#rec").show();
                    Recording('start');                                          
                    $(".readSensors").prop('disabled', true); 
                    $(".dwldButtons").addClass('disabled');                   
             }   
                     
            $(idPicker).prop('disabled', true);
            $(idPicker).selectpicker('refresh');
            $(this).addClass('running');
            $(this).children('i').removeClass('text-success').removeClass('fa-play');
            $(this).children('i').addClass('text-danger').addClass('fa-stop');
            $(this).children('span').html('Stop');
            
        }
    });
    
    
    function stopReading(){
        window.clearInterval(pingPong);
        socket.close();
    }

    /*This variable maps each sensor with the corresponding channel
     * and the message content (the data) with the corresponding graph.  */
    var socketChannelMap = {
        'IMU_acc': {
            'channelName':'IMU_data',
            'chartObjects': {
                'buff_acc' : IMU12,
                'buff_vel' : IMUangVel,
            },
            'leader':true
        },
        'IMU_vel': {
            'channelName':'IMU_data',
            'chartObjects': {
                'buff_acc' : IMU12,
                'buff_vel' : IMUangVel,
            }
        },
        'Razor_acc': {
            'channelName':'RazorIMU_data',
            'chartObjects': {
                'buff_acc' : RazorIMU,
                'buff_vel' : RazorIMUvel,
            }
        },
        'Razor_vel': {
            'channelName':'RazorIMU_data',
            'chartObjects': {
                'buff_acc' : RazorIMU,
                'buff_vel' : RazorIMUvel,
            }
        },
        'Load_Cell': {
            'channelName':'LoadCell_data',
            'chartObjects': {
                'data' : LoadCell
            }
        },
        'CAN':{
           'channelName':'CAN_data',
            'chartObjects': {
                'data' : CAN
            } 
        }
    }
    
    var pingPong;
    
    /* Create a socket instance, and listen on the sensors channels */
    function startReading(){

        var startedChannels = [];
        var selectedSensors = $('#selectReadings').val();
        
        socket = io(namespace);   
        
        var ping_pong_times = [];
        var start_time;     
           
        socket.on('connect', function() {
                socket.emit('my_event', {data: 'connected from charts'});
                ping_pong_times = [];
        });
            
        // Tests message latency by sending a "ping"
        // message. The server then responds with a "pong" message and the
        // round trip time is measured.
      
        pingPong = window.setInterval(function() {
            start_time = (new Date).getTime();
            socket.emit('my_ping');
        }, 1000);
        
        // Handler for the "pong" message. When the pong is received, the
        // time from the ping is stored, and the average of the last 30
        // samples is average and displayed.
        socket.on('my_pong', function() {
            var latency = (new Date).getTime() - start_time;
            ping_pong_times.push(latency);
            ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
            var sum = 0;
            for (var i = 0; i < ping_pong_times.length; i++)
                sum += ping_pong_times[i];
            $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
        }); 
   
        /*Change buttons appearance if someone is already recording */
        socket.on('busy', function(msg) {        
            if(msg){
              isRecording = msg.isRecording   
            }    
            else{
                isRecording = !isRecording;                
            }  
            prop= isRecording?true:false;
            $(".recordSensors").prop('disabled', prop);                  
            if(isRecording){
                $(".recordSensors").children('span').html('In Use'); 
                $("#rec").children('span').eq(1).text(" Already recording...")
                $("#rec").show();
                $(".dwldButtons").addClass('disabled');
            }
            else{
            $(".recordSensors").children('span').html('Start');
            $("#rec").children('span').eq(1).text(" Recording...")
            $("#rec").hide(); 
            $(".dwldButtons").removeClass('disabled');
            }
            
        });
        
        /*Go through the socketChannelMap and for each sensor check if 
         * it is selected. If that's the case, add its channel to startedChannels.
         * First if statement avoids to add the same channel multiple times, second one
         * avoids listening on unselected channels.
         *   */    
        $.each(socketChannelMap, function(sensorName, value) {
            if(startedChannels.includes(value.channelName)){
                return;
            }
            if(!selectedSensors.includes(sensorName)){
                return;
            }
            startedChannels.push(value.channelName);
            
        /*This function fires each time a new message (response) is sent on a channel.
          The new data and the corresponding chart object are given as argument 
          to updateResponse. */    
        socket.on(value.channelName, function (response) {
                if(response){
                    response = JSON.parse(response);
                    updateResponse(value.chartObjects,response);
                }
            });
        });

    }  
    
    /* Send to Flask server the action to execute when recording (start or stop)
     * and the concerned sensors.*/
    function Recording(action){
        var selectedSensors = $('#selectRecordings').val();        
        socket.emit('record',[action, selectedSensors]);
    }    
    
    /*Stop reading (and recording) if the user closes the window*/
  $(window).on("unload",function(){    
       if ($(".recordSensors").hasClass('running')) {                   
            socket.emit('record',['stop', $('#selectRecordings').val()]); 
        }            
            stopReading() ;        
        });
    /* Give to the function drawGraph the chart object to update and the
     * new values*/
    function updateResponse(chartObjects, response){
      $.each(chartObjects, function( responseName, chartObject) {
        drawGraph(chartObject, response[responseName], false);
      });
    }
    
    /*Fire when the "Set" button is clicked. Send motors command to Flask
     * server. */    
    $(".set").click(function(){     
        var commands = {};
        var inputs = document.getElementsByClassName('form-control');
        for (var i = 0; i < inputs.length; i++){            
            if (inputs[i].value){ 
                commands[inputs[i].name] =  inputs[i].value;
            }                        
        }
        socket.emit('motorCommands',commands);           
    });
})
