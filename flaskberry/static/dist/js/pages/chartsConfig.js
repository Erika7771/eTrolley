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

    $(".reloadIMU12").click(function () {
        updateIMU12();
    });


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

    var $IMUsf = $('#IMUsf');
    var IMUsf = new Chart($IMUsf, {
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

    var $IMUsfvel = $('#IMUsfvel')
    var IMUsfvel = new Chart($IMUsfvel, {
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

    $('#selectReadings').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
        var latest_value = $('#selectReadings option').eq(clickedIndex).val();
        var latest_selection = isSelected;
        if(latest_value=='all' && latest_selection){
            $(this).parents('.selectpicker').selectpicker('selectAll');
        }else if(latest_value=='all' && !latest_selection){
            $(this).parents('.selectpicker').selectpicker('deselectAll');
        }
    });

    $("#selectReadings").change(function(){
        //if(){
        //    .includes("Mango");
        //    .length
        //}
        //console.log($(this).val());
    });


})
