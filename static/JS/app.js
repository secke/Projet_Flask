fetch('/donnes')
  .then(function (reponse) {
      return reponse.json();
  }).then(function (text) {

    dataset=text
    const width = 900;
    const height = 450;
    const margin = { top: 50, bottom: 50, left: 50, right: 50 };

    const svg=d3.select('#container-d3')
                .append('svg')
                .attr('width',width-margin.left-margin.right)
                .attr('heght',height-margin.top-margin.bottom)
                .style('background-color','lightgrey')
                .attr('viewBox',[0,0,width,height]);
  })

  

  




//   var svg = d3.select("body")
//   .append("svg")
//   .attr("width", 900)
//   .attr("height", 450)
//   .attr('class','svg1')
//   .style('background-color', 'lightgrey');

// svg.selectAll('.bar')
//   .data(dataset)
//   .enter()
//   .append('rect')
//   .attr('class','rect1')
//   .attr('x', (d,i) => i*25 )
//   .attr('y', 0)
//   .attr('width', 20)
//   .attr('height', (d) => d)
//   .attr('y',(d)=>100-d);
