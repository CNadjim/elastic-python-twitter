
// var data = [10, 20, 100];
var data = [];

d3.csv("./csv/lang_ARS.csv", function(error, data) {

  Object.entries(data[0]).forEach(entry => {
    el = parseInt(entry[1]);
    data.push(el);
  });
  data = data.slice(1, 7);

  var width = 760,
  height = 300,
  radius = Math.min(width, height) / 2;

  var color = d3.scaleOrdinal()
  .range([ "#6d3580", "#cc4165", "#e4734f", "#ffe26f", "#00a8b5", "#de4383" ]);

  var arc = d3.arc()
  .outerRadius(radius - 10)
  .innerRadius(0);

  var labelArc = d3.arc()
  .outerRadius(radius - 40)
  .innerRadius(radius - 40);

  var pie = d3.pie()
  .sort(null)
  .value(function(d) { return d; });

  var svg = d3.select("#arsenal").append("svg")
  .attr("class", "pie-chart")
  .attr("width", width)
  .attr("height", height)
  .append("g")
  .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var g = svg.selectAll(".arc")
  .data(pie(data))
  .enter().append("g")
  .attr("class", "arc");

  g.append("path")
  .attr("d", arc)
  .style("fill", function(d) { return color(d.data); });

  g.append("text")
  .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
  .attr("dy", ".35em")
  .text(function(d) { return d.data; });
});
