var acmeDrawGraph = function() {
    var profits = {};
    
    // Q1-Q2: get innerHTML, remove €
    var value = document.getElementById('acme-q1').innerHTML;
    if( value[value.length-1] == "€" ) value = value.substring(0, value.length-1);
    profits['q1'] = value;
    var value = document.getElementById('acme-q2').innerHTML;
    if( value[value.length-1] == "€" ) value = value.substring(0, value.length-1);
    profits['q2'] = value;
    
    // Q3-Q4: get input.value
    profits['q3'] = document.getElementById('acme-q3').value;
    profits['q4'] = document.getElementById('acme-q4').value;

    // Convert all to numeric value, and remember max value for scaling purposes.
    var max = profits['q1'];
    for ( var q in profits ) {
        profits[q] = isNaN(profits[q]) ? 0 : Number(profits[q]);
        if( profits[q] > max ) {
            max = profits[q];
        }
    }
    
    // Draw the bar graph
    for ( var q in profits ) {
        var h = 200 * profits[q] / max;
        var div = document.getElementById('acme-graph-'+q);
        div.style = 'height: ' + h + 'px';
    }
};

var rootElement = document.getElementById( "impress" );
rootElement.addEventListener( "impress:init", function() {
  acmeDrawGraph();
});