function interpolateArray(data, fitCount) {
    
    var linearInterpolate = function (before, after, atPoint) {
        return before + (after - before) * atPoint;
    };
    
	var newData = new Array();
	var springFactor = new Number((data.length - 1) / (fitCount - 1));
	newData[0] = data[0]; // for new allocation
	for ( var i = 1; i < fitCount - 1; i++) {
		var tmp = i * springFactor;
		var before = new Number(Math.floor(tmp)).toFixed();
		var after = new Number(Math.ceil(tmp)).toFixed();
		var atPoint = tmp - before;
		newData[i] = linearInterpolate(data[before], data[after], atPoint);
		}
	newData[fitCount - 1] = data[data.length - 1]; // for new allocation
	return newData;
};

$(function () {
    'use strict'

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
    
    var optStyle2 = {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                gridLines: {
                    display: true
                },
                ticks: $.extend({
                    beginAtZero: true,
                    suggestedMax: 3
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
     var optStyle3 = {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                gridLines: {
                    display: true
                },
                ticks: $.extend({
                    beginAtZero: true,
                    suggestedMax: 300
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
    
     var optStyle4 = {
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                gridLines: {
                    display: true
                },
                ticks: $.extend({
                    beginAtZero: true,
                    suggestedMax : 10000
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
    
    

    var timer;

    var namespace = '/sensors';
    var socket = io(namespace);
    socket.close();

    var zero = 0;
    var readyToRequest = true;

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

    var $Arduino = $('#Arduino')
    var Arduino = new Chart($Arduino, {
        type: 'line',
        data: {
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            }]
        },
        options: optStyle
    })
        //This event fires after the select's value has been changed.
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
            $("#downlaodFiles").attr("href","/recordings/last_recording?data="+sensorsToken+"&rnd="+Math.random());
        }

    });

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

    $(".readSensors, .recordSensors").click(function(){
        
        var reading = $(this).hasClass("readSensors");
        var idPicker = reading?'#selectReadings':"#selectRecordings";
        
        if ($(this).hasClass('running')) {

            if(reading){
                stopReading();
            }else{
                Recording('stop');
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
                Recording('start');
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
        socket.close();
    }

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
    }

    function startReading(){

        var startedChannels = [];
        var selectedSensors = $('#selectReadings').val();
        
        socket = io(namespace);

        $.each(socketChannelMap, function( sensorName, value) {
            if(startedChannels.includes(value.channelName)){
                return;
            }
            if(!selectedSensors.includes(sensorName)){
                return;
            }
            startedChannels.push(value.channelName);
            socket.on(value.channelName, function (response) {
                if(response){
                    response = JSON.parse(response);
                    updateResponse(value.chartObjects,response);
                }
            });
        });

    }
    
    function Recording(action){
        var startedChannels = [];
        var selectedSensors = $('#selectRecordings').val();
        
        socket.emit('record',[action, selectedSensors])
    }
    
    
    function updateResponse(chartObjects, response){
      $.each(chartObjects, function( responseName, chartObject) {
        drawGraph(chartObject, response[responseName], false);
      });
    }



})
