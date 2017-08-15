function test(test_url) {
    colors = [ 
        '#1f77b4',  // muted blue
        '#ff7f0e',  // safety orange
        '#2ca02c',  // cooked asparagus green
        '#d62728',  // brick red
        '#9467bd',  // muted purple
        '#8c564b',  // chestnut brown
        '#e377c2',  // raspberry yogurt pink
        '#7f7f7f',  // middle gray
        '#bcbd22',  // curry yellow-green
        '#17becf'   // blue-teal
    ];

    var configData = {
        title: "",
        xlabel: "",
        ylabel: "",
        data: {},
        errorLineMode: 'lines',
        lineMode: 'lines+markers',
        errorBars: false
    };

    $('#show-error').change(function () {
        redraw();
    });

    $("#test1Button").click(function (ev) {
        configData = {
            title: "Test 1: Gene expression (tissues: AM, LUNG) (Flu: F150)",
            xlabel: "Age (months)",
            ylabel: "Expression (unit)",
            data: {dataset: "mouse_aging",
                   xaxis: "age",
                   series: "gene",
                   restrictions: [["tissue", "in", ["AM", "LUNG"]],
                                  ["flu", "eq", "F150"],
                                  ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]]},
            errorLineMode: 'lines',
            lineMode: 'lines+markers',
            errorBars: false
        };
        redraw();
    });

    $("#test2Button").click(function (ev) {
        configData = {
            title: "Test 3: Gene expression",
            xlabel: "Tissue",
            ylabel: "Expression (unit)",
            data: {dataset: "mouse_aging",
                   xaxis: "tissue",
                   series: "gene",
                   restrictions: [
                      ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]],
                      ["age", "eq", 12]]},
            errorLineMode: null,
            lineMode: 'markers',
            errorBars: true
        };
        redraw();
        // configData = {
        //     title: "Test 2: Gene expression (Flu: F150)",
        //     xlabel: "Age (months)",
        //     ylabel: "Expression (unit)",
        //     data: {xaxis: "age",
        //           series: "tissue",
        //           restrictions: [["flu", "eq", "F150"],
        //                          ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]]},
        //     errorLineMode: null,
        //     lineMode: 'lines+markers',
        //     errorBars: false
        // };
        // redraw();
    });

    $("#test3Button").click(function (ev) {
        configData = {
            title: "Test 3: Gene expression",
            xlabel: "Tissue",
            ylabel: "Expression (unit)",
            data: {dataset: "mouse_aging",
                  xaxis: "tissue",
                  series: "gene",
                  restrictions: [
                      ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]],
                      ["age", "eq", 4]]},
            errorLineMode: null,
            lineMode: 'markers',
            errorBars: true
        };
        redraw();
    });

    function redraw() {
        data = configData['data'];
        errorLineMode = configData['errorLineMode'];
        lineMode = configData['lineMode'];
        errorBars = configData['errorBars'];
        title = configData['title'];
        xlabel = configData['xlabel'];
        ylabel = configData['ylabel'];

        $.ajax({
            type: 'post',
            url: test_url,
            beforeSend: function (xhr, settings) {
                var csrftoken = $("[name='csrfmiddlewaretoken']").val();
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data: JSON.stringify(data)
        }).done(function (data) {
            var xvalues = data["xvalues"];
            var series = data["series"];
            mainCanvas = document.getElementById('main-canvas');
            var plots = [];
            $.each(series, function(index, current) {
                var name = current["name"];
                var values = current["values"];
                var ymean = [];
                var ystd = [];
                var ymin = [];
                var ymax = [];
                var color = colors[index % colors.length];

                $.each(values, function(index, value) {
                    var mean = value[0];
                    var std = value[1];
                    ymean.push(mean);
                    ystd.push(std);
                    ymin.push(mean - std);
                    ymax.push(mean + std);
                });

                if (errorLineMode != null) {
                    plots.push({
                        mode: errorLineMode,
                        line: {shape: 'spline', color: color, width: 0},
                        showlegend: false,
                        x: xvalues,
                        y: ymin,
                        hoverinfo: "none",
                        fill: null,
                    });
                    plots.push({
                        mode: errorLineMode,
                        line: {shape: 'spline', color: color, width: 0},
                        showlegend: false,
                        x: xvalues,
                        y: ymax,
                        hoverinfo: "none",
                        fill: 'tonexty',
                        opacity: 0.5
                    });
                }

                if (errorBars) {
                    plots.push({
                        mode: lineMode,
                        line: {shape: 'spline', color: color},
                        name: name,
                        x: xvalues,
                        y: ymean,
                        error_y: {type: 'data', array: ystd, visible: true}
                    });
                } else {
                    plots.push({
                        mode: lineMode,
                        line: {shape: 'spline', color: color},
                        name: name,
                        x: xvalues,
                        y: ymean
                    });

                }
            });

            var defaultPlotlyConfiguration = { 
                displayModeBar: true,
                modeBarButtonsToRemove: [
                    'sendDataToCloud', 
                    'autoScale2d', 
                    'hoverClosestCartesian', 
                    'hoverCompareCartesian', 
                    'lasso2d', 
                    'select2d'], 
                displaylogo: false, 
                showTips: false };
            Plotly.newPlot(mainCanvas, plots, {
                title: title,
                yaxis: {title: ylabel},
                xaxis: {title: xlabel}
                // margin: { t: 0 } 
            }, defaultPlotlyConfiguration);
        });
    };
}