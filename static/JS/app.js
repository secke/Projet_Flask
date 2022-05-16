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
  //  .join("rect")
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

    // dataset=text
    var width = 900;
    var height = 450;
    var margin = { top: 50, bottom: 50, left: 50, right: 50 };
    
    // console.log(dataset)
    const svg=d3.select('#container-d3')
                .append('svg')
                .attr('width',width-margin.left-margin.right)
                .attr('heght',height-margin.top-margin.bottom)
                .style('background-color','lightgrey')
                .attr('viewBox',[0,0,width,height]);
  

// ***********************diagramme circulaire des photos par album***********************//

// ######## Recuperation des donnees sur un fichier json creer sur le fichier python et la fonction permettant l'affichage ########

d3.json("../static/data.json", function (data) {
  // console.log('bab : ',data);

// ###### variable de dimentionnement ###########

var width = 600
    height =600
    margin = 40


var radius = Math.min(width, height) / 2 - margin
// ##### recuperation de la division devant recevoir le diagramme et ajout des balises svg parent de g ######
var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

console.log(svg)

// var data = {a: 9, b: 20, c:30, d:8, e:12, f:17, g:20, h:12, i:8, j:13}

// ### Generation d'une couleur pour chaque portion du diagramme ####

var color = d3.scaleOrdinal()
  .domain(data)
  .range(d3.schemeSet2);

// ### Transformation de la valeur de chaque section en un rayon
// ### Associer à la fonction d3.arc() fournit un angle corespondant

var pie = d3.pie()
  .value(function(d) {return d.value; })
var data_ready = pie(d3.entries(data))

var arcGenerator = d3.arc()
  .innerRadius(0)
  .outerRadius(radius)

// #### Selectionner l'ensemble des element de section, generer un arc et appliquer une couleur #######

svg
  .selectAll('mySlices')
  .data(data_ready)
  .enter()
  .append('path')
    .attr('d', arcGenerator)
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)
 


// ########## selectionner l'ensemble des elements et appliquer le label correspondant ###############

svg
  .selectAll('mySlices')
  .data(data_ready)
  .enter()
  .append('text')
  .text(function(d){ return  d.data.key})
  .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
  .style("text-anchor", "middle")
  .style("font-size", 17)

  });

// ////////////////////////////

var nwidth=400
nheight=400


 
  

//
