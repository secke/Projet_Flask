var width = 1000,
  height = 500;
afaire=document.querySelectorAll("#A_faire").length;
encours=document.querySelectorAll("#En_cours").length;
termine=document.querySelectorAll("#Termine").length;
total=afaire+encours+termine

var couleur = d3.scaleOrdinal(d3.schemeCategory10); 
var svg = d3
  .select(".graph")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .style("background", "#F5D7FF");
var data = [
  { Type: "A faire", Nbr: afaire },
  { Type: "En cours", Nbr: encours },
  { Type: "Termine", Nbr: termine},
];
var base_diagramme = d3.pie().value(function (d) {
  return d.Nbr;
})(data);

var segments = d3
  .arc()
  .innerRadius(0)
  .outerRadius(200)
  .padAngle(0.05)
  .padRadius(50);

var sections = svg
  .append("g")
  .attr("transform", "translate(250,250)")
  .selectAll("path")
  .data(base_diagramme);
sections.enter().append("path").attr("d", segments)
 .attr("fill", function (d) {
    return couleur(d.data.Nbr);
  });


var libelle = d3.select("g")
.selectAll("text")
.data(base_diagramme);
libelle.enter()
  .append("text")
  .classed("inside", true)
  .each(function(d){
var center = segments.centroid(d);
 // console.log(center)
  d3.select(this)
  .attr("x", center[0])
  .attr("y", center[1])
  .text(d.data.Nbr);});

var legends=svg.append("g")
.attr("transform","translate(500,200)")
.selectAll(".legends")
.data(base_diagramme);
var legend = legends.enter()
.append("g")
.classed("label", true)
.attr("transform", function(d,i){
  return "translate(0," + (i+1)*50 + ")";
});
legend.append("rect")
  .attr("width", 20)
  .attr("height", 20)
  .attr("fill", function(d){
  return couleur(d.data.Nbr);
});
legend.append("text")
  .classed("label", true)
.style("fill", "black")
  .text(function(d){
  return d.data.Type;
})
.attr("fill", function(d){
  return couleur(d.data.Nbr);
})
.attr("x", 30)
.attr("y", 15);
svg.append("text")
.attr("x", 400)
.attr("y", 25)
.attr("text-anchor", "middle")
.style("font-size", "30px")
.style("fill", "#AE25DE")
.style("text-decoration", "underline")
.text("Diagramme Circulaire");




































// afaire=document.querySelectorAll("#A_faire").length;
// encours=document.querySelectorAll("#En_cours").length;
// termine=document.querySelectorAll("#Termine").length;
// total=afaire+encours+termine

// const width=400;
// const height=400;
// data=[afaire,encours,termine]
// texte=["A faire","En cours","Terminé"]
// var svg= d3.select("#circ")
//            .append("svg")
//            .attr('width',width )
//            .attr('height',height );
// radius = Math.min(width, height) / 2,
//         g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

//     var color = d3.scaleOrdinal(['red','orange','green']);

//     var pie = d3.pie();

//     var arc = d3.arc()
//                 .innerRadius(0)
//                 .outerRadius(radius);

//     //Generate groups
//     var arcs = g.selectAll("arc")
//                 .data(pie(data))
//                 .enter()
//                 .append("g")
//                 .attr("class", "arc")

//     //Draw arc paths
//     arcs.append("path")
//         .attr("fill", function(d, i) {
//             return color(i);
//         })
//         .attr("d", arc);

    











 