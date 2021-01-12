// Submit Button handler
function handleSubmit() {
  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input value from the form
  var article = d3.select("#stockInput").node().value;
  console.log(article;

  // clear the input value
  d3.select("#stockInput").node().value = "";

  // Build the plot with the new stock
  buildPlot(article);
}

function buildPlot(article) {
  var apiKey = NYT_KEY;

  var url = `https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=${apiKey}&q=${article}&begin_date=2016-01-12&end_date=2021-01-12`;

  d3.json(url).then(function(data) {
    // Grab values from the response json object to build the plots
    var 