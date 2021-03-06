/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Close
 * index 5 - Volume
 */

// Submit Button handler
function handleSubmit() {
  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input value from the form
  var stock = d3.select("#stockInput").node().value;
  console.log(stock);

  // clear the input value
  d3.select("#stockInput").node().value = "";

  // Build the plot with the new stock
  buildPlot(stock);
}

function buildPlot(stock) {
  var apiKey = API_KEY;

  var url = `https://www.quandl.com/api/v3/datasets/EOD/${stock}.json?start_date=2011-01-11&end_date=2021-01-11&api_key=${apiKey}`;

  d3.json(url).then(function(data) {
    // Grab values from the response json object to build the plots
    var name = data.dataset.name;
    var stock = data.dataset.dataset_code;
    var startDate = data.dataset.start_date;
    var endDate = data.dataset.end_date;
    // Print the names of the columns
    console.log(data.dataset.column_names);
    // Print the data for each day
    console.log(data.dataset.data);
    var dates = data.dataset.data.map(row => row[0]);
    // console.log(dates);
    var closingPrices = data.dataset.data.map(row => row[4]);
    // console.log(closingPrices);

    var trace1 = {
      type: "scatter",
      mode: "lines",
      name: name,
      x: dates,
      y: closingPrices,
      line: {
        color: "#17BECF"
      }
    };

    var data = [trace1];

    var layout = {
      title: `${stock} closing prices`,
      xaxis: {
        autorange: true,
        range: [startDate, endDate],
        rangeselector: {buttons: [
          {
            count: 1,
            label: 'Daily',
            step: 'day',
            stepmode: 'backward'
          },
          {
            count: 366,
            label: '1 Year',
            step: 'day',
            stepmode: 'backward'
          },
          {
            count: 1827,
            label: '5 Year',
            step: 'day',
            stepmode: 'backward'
          },
          {
            count: 3653,
            label: '10 Year',
            step: 'day',
            stepmode: 'backward'
          },
          {step: 'all'}
        ]},
        rangeslider: {range: [startDate, endDate]},
        type: "date"
      },
      yaxis: {
        autorange: true,
        type: "linear"
      }
    };

    Plotly.newPlot("plot", data, layout);

  });
}

// Add event listener for submit button
d3.select("#submit").on("click", handleSubmit);
