fetch('/donnes')
  .then(function (reponse) {
      return reponse.json();
  }).then(function (text) {
   
  const dataset=text
 
  const width = 2000;
  const height = 450;
  const margin = { top: 50, bottom: 50, left: 50, right: 50 };


   const svg=d3.select('#container-d3')
     .append('svg')
     .attr('width',width-margin.left-margin.right)
     .attr('heght',height-margin.top-margin.bottom)
     .style('background-color','#F5D7FF')
     .attr('viewBox',[0,0,width,height]);
   
   const x=d3.scaleBand()
   .domain(d3.range(dataset.length))
   .range([margin.left, width - margin.right])
   .padding(0.1)
   
   const y = d3.scaleLinear().domain([0, 10]).range([height - margin.bottom, margin.top]);

   
   svg
   .append("g")
   .attr("fill",'blueviolet')
   .selectAll("rect")
   .data(dataset.sort((a, b) => d3.descending(a.nbr, b.nbr)))
   .join("rect")
   .attr("x", (d, i) => x(i))
   .attr("y", d => y(d.nbr))
   .attr('title', (d) => d.nbr)
   .attr("class", "rect")
   .attr("height", d => y(0) - y(d.nbr))
   .attr("width", x.bandwidth());
   
   
   function yAxis(g) {
   g.attr("transform", `translate(${margin.left}, 0)`)
   .call(d3.axisLeft(y).ticks(null, dataset.format))
   .attr("font-size", '20px')
   }
   
   function xAxis(g) {
   g.attr("transform", `translate(0,${height - margin.bottom})`)
   .call(d3.axisBottom(x).tickFormat(i => dataset[i].name))
   .attr("font-size", '15px')
   }
   
   svg.append("g").call(xAxis);
   svg.append("g").call(yAxis);
   svg.node();
   
   




   
  
  })




// ////////////////////////////

var nwidth=400
nheight=400


 
  

//
