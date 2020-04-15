$(function () {
  'use strict'

  var ticksStyle = {
    fontColor: '#495057',
    fontStyle: 'bold'
  }

  var mode      = 'index'
  var intersect = true  
  
  
  $(".reloadIMU12").click(function(){
    updateIMU12();
  });
    
    
  var timer;
  
  var namespace = '/sensors';
  var socket = io(namespace);
  socket.close();
  

  $(".monitorIMU12").click(function(){
    
    if($(this).hasClass('running')){
      socket.close();
      $(this).removeClass('running');
      $(this).removeClass('text-warning');
    }else{
      socket = io(namespace);
      socket.on('IMU_data', function(response, cb) {
        response = JSON.parse(response);
        drawGraph(IMU12,response.buff_acc,false);
        drawGraph(IMUangVel,response.buff_vel,true);
      });
      $(this).addClass('running');
      $(this).addClass('text-warning');
    }
  });

  var zero = 0;
  var readyToRequest = true;

  function drawGraph(graph,newData,checkReady){    
    var i;
    var j;
    var tooLong = graph.data.datasets[0].data.length > 300;
    
    for(i = 0; i < newData.length; i++){
      graph.data.labels.push(zero);
      if(tooLong){
        graph.data.labels.splice(0, 1);
      }
      for (j = 0; j < graph.data.datasets.length; j++) {
        if(tooLong){
          graph.data.datasets[j].data.splice(0, 1);
        }
        graph.data.datasets[j].data.push(newData[i][j]); 
      }      
      zero++;
    }
    graph.update();
  }  

  var $IMU12 = $('#IMU12');
  var IMU12  = new Chart($IMU12, {
    type: 'line',
    backgroundColor: 'transparent',
    data: {
      //labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
        type                : 'line',
        data                : [10, 12, 17, 26, 18, 15, 16],
        
        borderColor         : '#6BC1FF',
        pointBorderColor    : '#6BC1FF',
        pointBackgroundColor: '#6BC1FF',
        fill                : false
      },
      {        
        data                : [30, 80, 310, 97, 80, 33, 100],
        borderColor         : '#52FF89',
        pointBorderColor    : '#52FF89',
        pointBackgroundColor: '#52FF89',
        fill                : false
      },
      {
        data                : [34, 262, 73, 59, 30, 20, 80],
        borderColor         : '#FF7A78',
        pointBorderColor    : '#FF7A78',
        pointBackgroundColor: '#FF7A78',
        fill                : false
      }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      animation: false,
      maintainAspectRatio: false,
      tooltips: {
        enable: false
      },
      hover: {
        mode: null
      },
      legend: {
        display: false
      },
      elements: {
        point: {
          radius: 0
        }
      },
      scales: {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 1000
          }, ticksStyle)
        }],
        xAxes: [{          
          display: true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
          gridLines: {
            display: true
          },
          ticks: ticksStyle
        }]
      }
    }
  })  
  
  
  var $IMUangVel = $('#IMUangVel')
  var IMUangVel  = new Chart($IMUangVel, {
    data   : {
      labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
    type                : 'line',
    data                : [10, 12, 17, 26, 18, 15, 16],
    backgroundColor     : 'transparent',
    borderColor         : '#6BC1FF',
    pointBorderColor    : '#6BC1FF',
    pointBackgroundColor: '#6BC1FF',
    fill                : false
      },
        {
          type                : 'line',
          data                : [30, 80, 310, 97, 80, 33, 100],
          backgroundColor     : 'tansparent',
          borderColor         : '#52FF89',
          pointBorderColor    : '#52FF89',
          pointBackgroundColor: '#52FF89',
          fill                : false
        },
        {
          type                : 'line',
          data                : [34, 262, 73, 59, 30, 20, 80],
          backgroundColor     : 'tansparent',
          borderColor         : '#FF7A78',
          pointBorderColor    : '#FF7A78',
          pointBackgroundColor: '#FF7A78',
          fill                : false
        }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      animation : false,
      maintainAspectRatio: false,
      tooltips           : {
        enable: false
      },
      hover              : {
        mode     : null
      },
      legend             : {
        display: false
      },
      elements: {
    point: {
      radius: 0
    }
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display: true,
        scaleLabel: {
          display: true,
          labelString: "Time",
        },
          gridLines: {
            display: true
          },
          ticks: ticksStyle
        }]
      }
    }
  })  

  var $IMUsf = $('#IMUsf');
  var IMUsf  = new Chart($IMUsf, {
    data   : {
      labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
        type                : 'line',
        data                : [110, 100, 150, 190, 150, 180, 150],
        backgroundColor     : 'transparent',
        borderColor         : '#6BC1FF',
        pointBorderColor    : '#6BC1FF',
        pointBackgroundColor: '#6BC1FF',
        fill                : false
      },
        {
          type                : 'line',
          data                : [450, 90, 100, 50, 30, 90, 110],
          backgroundColor     : 'tansparent',
          borderColor         : '#52FF89',
          pointBorderColor    : '#52FF89',
          pointBackgroundColor: '#52FF89',
          fill                : false
        },
        {
          type                : 'line',
          data                : [6, 80, 40, 68, 21, 120, 70],
          backgroundColor     : 'tansparent',
          borderColor         : '#FF7A78',
          pointBorderColor    : '#FF7A78',
          pointBackgroundColor: '#FF7A78',
          fill                : false
        }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
          gridLines: {
            display: true
          },
          ticks    : ticksStyle
        }]
      }
    }
  })
  
  var $IMUsfvel = $('#IMUsfvel')
  var IMUsfvel  = new Chart($IMUsfvel, {
    data   : {
      labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
        type                : 'line',
        data                : [143, 42, 1, 265, 18, 88, 16],
        backgroundColor     : 'transparent',
        borderColor         : '#6BC1FF',
        pointBorderColor    : '#6BC1FF',
        pointBackgroundColor: '#6BC1FF',
        fill                : false
      },
        {
          type                : 'line',
          data                : [30, 8, 31, 97, 32, 33, 80],
          backgroundColor     : 'tansparent',
          borderColor         : '#52FF89',
          pointBorderColor    : '#52FF89',
          pointBackgroundColor: '#52FF89',
          fill                : false
        },
        {
          type                : 'line',
          data                : [34, 21, 73, 23, 90, 20, 80],
          backgroundColor     : 'tansparent',
          borderColor         : '#FF7A78',
          pointBorderColor    : '#FF7A78',
          pointBackgroundColor: '#FF7A78',
          fill                : false
        }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
          gridLines: {
            display: true
          },
          ticks    : ticksStyle
        }]
      }
    }
  })  
  
  var $loadCell = $('#loadCell')
  var loadCell  = new Chart($loadCell, {
    data   : {
      labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
        type                : 'line',
        data                : [100, 10, 170, 167, 1840, 177, 160],
        backgroundColor     : 'transparent',
    borderColor         : '#6BC1FF',
        pointBorderColor    : '#6BC1FF',
        pointBackgroundColor: '#6BC1FF',
        fill                : false
      }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
          gridLines: {
            display: true
          },
          ticks    : ticksStyle
        }]
      }
    }
  })   
  
  var $Arduino = $('#Arduino')
  var Arduino  = new Chart($Arduino, {
    data   : {
      labels  : ['1', '2', '3', '4', '5', '6', '7'],
      datasets: [{
        type                : 'line',
        data                : [10, 110, 10, 267, 180, 172, 16],
        backgroundColor     : 'transparent',
        borderColor         : '#6BC1FF',
        pointBorderColor    : '#6BC1FF',
        pointBackgroundColor: '#6BC1FF',
        fill                : false
        // pointHoverBackgroundColor: '#6BC1FF',
        // pointHoverBorderColor    : '#6BC1FF'
      }]
    },
    options: {
      //elements:{
    //line:{
      //tension:0
    //}
      //},
      maintainAspectRatio: false,
      tooltips           : {
        mode     : mode,
        intersect: intersect
      },
      hover              : {
        mode     : mode,
        intersect: intersect
      },
      legend             : {
        display: false
      },
      scales             : {
        yAxes: [{
          // display: false,
          gridLines: {
            display      : true,
          },
          ticks    : $.extend({
            beginAtZero : true,
            suggestedMax: 200
          }, ticksStyle)
        }],
        xAxes: [{
          display  : true,
          scaleLabel: {
            display: true,
            labelString: "Time",
          },
          gridLines: {
            display: true
          },
          ticks    : ticksStyle
        }]
      }
    }
  })
})
