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
    

    var timer;

    var namespace = '/sensors';
    var socket = io(namespace);
    socket.close();

    $(".monitorIMU12").click(function () {

        if ($(this).hasClass('running')) {
            socket.close();
            $(this).removeClass('running');
            $(this).removeClass('text-warning');
        } else {
            socket = io(namespace);
            socket.on('IMU_data', function (response, cb) {
                response = JSON.parse(response);
                drawGraph(IMU12, response.buff_acc, false);
                drawGraph(IMUangVel, response.buff_vel, true);
            });
            $(this).addClass('running');
            $(this).addClass('text-warning');
        }
    });
    
    $(".monitorRazorIMU").click(function () {

        if ($(this).hasClass('running')) {
            socket.close();
            $(this).removeClass('running');
            $(this).removeClass('text-warning');
        } else {
            socket = io(namespace);
            socket.on('RazorIMU_data', function (response, cb) {
                response = JSON.parse(response);
                drawGraph(RazorIMU, response.buff_acc, false);
                drawGraph(RazorIMUvel, response.buff_vel, true);
            });
            $(this).addClass('running');
            $(this).addClass('text-warning');
        }
    });

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
        options: optStyle
        
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
        options: optStyle
    })

    var $loadCell = $('#loadCell')
    var loadCell = new Chart($loadCell, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                data: [],
                borderColor: '#6BC1FF'
            }]
        },
        options: optStyle
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

    });

    function renderSelectedGraphs(graphs){
        console.log(graphs);
        $(".card.sensor").hide();
        $.each(graphs, function( index, sensorName ) {
            $(".card.sensor[data-sensor='"+sensorName+"']").show();
        });
    }

    $(".readSensors").click(function(){
        if ($(this).hasClass('running')) {

            stopReading();

            $("#selectReadings").prop('disabled', false);
            $('#selectReadings').selectpicker('refresh');
            $(this).removeClass('running');
            $(this).children('i').removeClass('text-danger').removeClass('fa-stop');
            $(this).children('i').addClass('text-success').addClass('fa-play');
            $(this).children('span').html('Start');

        } else {

            //da lanciare i sockets selezionati

            $("#selectReadings").prop('disabled', true);
            $('#selectReadings').selectpicker('refresh');
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
            }
        },
        'IMU_vel': {
            'channelName':'IMU_data',
            'chartObjects': {
                'buff_acc' : IMU12,
                'buff_vel' : IMUangVel,
            }
        },
        'IMU_acc': {
            'channelName':'RazorIMU_data',
            'chartObjects': {
                'buff_acc' : RazorIMU,
                'buff_vel' : RazorIMUvel,
            }
        },
        'IMU_vel': {
            'channelName':'RazorIMU_data',
            'chartObjects': {
                'buff_acc' : RazorIMU,
                'buff_vel' : RazorIMUvel,
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
            socket.on(value.channelName, function (response, cb) {
                response = JSON.parse(response);

                $.each(value.chartObjects, function( responseName, chartObject) {
                    drawGraph(value.chartObject, response[responseName], false);
                }
            });
        });

    }



})
