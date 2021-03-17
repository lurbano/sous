
			onColor = 'rgba(255, 100, 100, 0.9)';
			offColor = 'rgba(100, 100, 255, 0.9)';
			selColor = 'rgba(0, 0, 0, 0.9)';

			iSel = 0;
			ptRadius = 3;
			selRadius = 7;
			hoverRadius = 5;

			get_T_ct = 0;
			l_on = false;
			Dt_start = 0;

			function update_xml_data_element(element){
				$("#"+element).html($xml.find(element).html());
			}
			function update_with_conversion(element, out_element, func) {
				var x = $xml.find(element).html();
				var y = func(x);
				$("#"+out_element).html(y);
			}

			function update_graph_data(tdata, cdata, rdata){
				lastX = tdata[tdata.length-1].x;
				lastY = tdata[tdata.length-1].y;
				t_chart.data.datasets[0].data = tdata;
				t_chart.data.datasets[0].pointBackgroundColor = cdata;
				t_chart.data.datasets[0].pointRadius = rdata;
				t_chart.data.datasets[1].data = [{x: tdata[iSel].x, y: lastY}, {x: lastX, y: lastY}];
				t_chart.update();
			}

			function generate_graph(tdata, cdata, rdata){
				//Generate graph
				ctx = $("#temp_graph");
				lastX = tdata[tdata.length-1].x;
				lastY = tdata[tdata.length-1].y;
				t_chart = new Chart(ctx, {
					type: 'scatter',
					data: {
						datasets: [{
							label: "Crockpot Temperature (deg. C)",
							pointBackgroundColor: cdata, //'rgba(255, 100, 100, 0.9)',
							pointRadius: rdata,
							pointHoverRadius: hoverRadius,
							data: tdata
						},
						{
							label: "Timer",
							showLine: true,
							data: [{x: tdata[iSel].x, y: lastY}, {x: lastX, y: lastY}]
						}]
					},
					options: {
						scales: {
							xAxes: [{
								//type: 'time',
								position: 'bottom'
								// time: {
								// 	unit: 'day',
								// 	unitStepSize: 1
								// }
							}],
							yAxes: [{
								scaleLabel: {
									display: true,
									labelString: "Degrees Celsius"
								}
							}]
						}
					}
				});

				ctx.click(function(e){
					var activePoints = t_chart.getElementsAtEvent(e);
					// $.each(activePoints[0], function(index, item) {
					// 	console.log(index+": "+item);
					//
					// });
					var i = activePoints[0]._index;
					iSel = i;
					set_web_com_parameter("iSel", i);
					var ptData = t_chart.data.datasets[0].data[i];
					//console.log("DATA: "+ptData);
					// $.each(ptData, function(index, item) {
					// 	console.log(index+": "+item);
					// });
					var i_last = t_chart.data.datasets[0].data.length - 1;
					var lastData = t_chart.data.datasets[0].data[i_last];
					var tsince = parseInt(lastData.x) - parseInt(ptData.x);
					console.log("last: "+lastData.x+" | point: "+ptData.x + " | since:"+ tsince);
					console.log("Time since:"+ secToDHMS(tsince));
					$("#Dt").html(time_since(ptData.x));
					t_chart.data.datasets[0].pointBackgroundColor[i] = selColor;
					t_chart.data.datasets[0].pointRadius[i] = selRadius;
					get_T_data(true);
				})

			}

			function time_since(t){
				Dt_start = parseInt(t);
				var i_last = t_chart.data.datasets[0].data.length - 1;
				var lastData = t_chart.data.datasets[0].data[i_last];
				var t_last = lastData.x;
				var tsince = parseInt(t_last) - Dt_start;
				return secToDHMS(tsince);
			}

			////////////////////
			function get_T_data(update){
				//$( "#T_table" ).html("retriving data ...");
				$.ajax({
					url: "./logs/T_data.txt",
					cache: false,
					success: function( data ) {
						var result = $.csv.toObjects(data);
						// $( "#T_table" ).html( JSON.stringify(result) );
						// $( "#T_table" ).append( '<p>' );



						var tdata = [];
						var cdata = [];
						var rdata = [];
						$.each(result, function(k, v){
							// $( "#T_table" ).append(k+": "+v+"<br>");
							// $( "#T_table" ).append("time="+v.time+", ");
							// $( "#T_table" ).append("T="+v.Temperature+"<br>");
							var tm = v.time/60;
							var T = v.Temperature;
							var pt = {x: tm, y: T};
							tdata.push(pt);
							rdata.push(ptRadius);

							if (v.l_on === "True"){
								cdata.push(onColor);
							} else {
								cdata.push(offColor);
							}
							if (k === iSel){
								cdata[iSel] = selColor;
								rdata[iSel] = selRadius;
							}



							// $.each(v, function(k1, v1){
							// 	$( "#T_table" ).append(k1+": "+v1+"| |");
							// });
						});

						if (update === true){
							update_graph_data(tdata, cdata, rdata);
						} else {
							generate_graph(tdata, cdata, rdata);
						}

						//var txt = "Graph updated at: "+result[result.length-1].time+", " + "T= " + result[result.length-1].Temperature + "<br>";

						//var txt = "Graph updated at: " + moment().toDate();
						//$( "#T_table" ).html(txt);

						//var result = $.csv.toArrays(data);
						//$( "#T_table" ).append( '<p>' );
						//$( "#T_table" ).append( JSON.stringify(result) );
					}
				});
			}

			function get_T_recent(){
				//$( "#T_table" ).html("retriving data ...");
				$.ajax({
					url: "./logs/current_data.json",
					dataType: "json",
					cache: false,
					success: function( data ) {
						//$( "#current" ).html( JSON.stringify(data) );

						//var txt = parseInt(data.time) + " sec.";
						var txt = secToDHMS(parseInt(data.time))

						$( "#time" ).html( txt );
						$( "#Temp" ).html( data.Temperature + " &deg;C" );
						//$( "#T_set" ).html( data.T_set + " &deg;C" );

						//$( "#Kp").html( data.Kp );
						//$( "#Kp_in" ).val( data.Kp );
						// $( "#Ki").html( data.Ki );
						// $( "#Kd").html( data.Kd );

						$( "#T_error").html( parseFloat(data.T_error).toFixed(2) );
						$( "#T_err_sum").html( data.T_err_sum.toFixed(2) );
						$( "#dT_err").html( parseFloat(data.dT_err).toFixed(4) );

						$( "#p_term").html( parseFloat(data.p_term).toFixed(3) );
						$( "#i_term").html( parseFloat(data.i_term).toFixed(3) );
						$( "#d_term").html( parseFloat(data.d_term).toFixed(3) );

						$( "#pidVal").html( parseFloat(data.pidVal).toFixed(3) );

						if (data.l_on){
							$( "#heat").html( "ON" );
							$( "#heat").css("background-color", onColor);
						} else {
							$( "#heat").html( "OFF" );
							$( "#heat").css("background-color", offColor);
						}

						$("#Dt").html(time_since(Dt_start));


					}
				});
			}

			function get_settings(){
				$.ajax({
					url: "./sets/web_com.json",
					dataType: "json",
					cache: false,
					success: function( data ) {
						$( "#set_T" ).html( data.set_T + " &deg;C" );
						if (typeof(data.Kp) !== 'undefined') {
							$( "#Kp_in").val( data.Kp);
							$( "#Ki_in").val( data.Ki);
							$( "#Kd_in").val( data.Kd);
						}
						iSel = data.iSel;
					}
				});
			}

			function set_Crockpot_button(){
				$.ajax({
					url: "./sets/web_com.json",
					dataType: "json",
					cache: false,
					success: function( data ) {
						if (data.runCrockpot === 1){
							$("#runCrock_but").val("Stop Crockpot");
							$("#CrockRunning").html("Running");
							l_on = true;
							iSel = 0; //for graph timer
							set_web_com_parameter("iSel", iSel);

						} else {
							$("#runCrock_but").val( "Start Crockpot");
							$("#CrockRunning").html("Off");
							l_on = false;
						}

					}
				});
			}

			function str_pad_left(string,pad,length) {
			    return (new Array(length+1).join(pad)+string).slice(-length);
			}
			function secToDHMS(secs){
				var dys = ~~(secs / (60*60*24))
				var hrs = ~~(secs / 3600);
    		var mins = ~~((secs % 3600) / 60);
    		var secs = secs % 60;
				return str_pad_left(hrs,"0", 2) + ":" + str_pad_left(mins,"0", 2) + ":" + str_pad_left(secs,"0", 2);
			}



			function update_graph(){
				var tdata = get_T_data();
				update_graph_data(tdata);
			}

			function get_T(){
				$.ajax({
					url: "./sets/web_com.json",
					dataType: "json",
					cache: false,
					success: function( data ) {
						get_T_ct++;
						//console.log("check: "+ data.check+":"+get_T_ct);
						if (data.check !== T_check_id) {
							var txt = data.Temperature + " &deg;C";

							$( "#T_check_output" ).html( txt );
							$( "#T_check_time" ).html( data.time );
							get_T_ct = 0;
						}
						else {
							$( "#T_check_output" ).html( "Requesting..." );
							$( "#T_check_time" ).html( data.time );
							setTimeout(function(){get_T();}, 500);

						}

					}
				});
			}

			function ajax_error(x,e){
				if (x.status==0) {
        	alert('You are offline!!\n Please Check Your Network.');
		    } else if(x.status==404) {
		        alert('Requested URL not found.');
		    } else if(x.status==500) {
		        alert('Internel Server Error.');
		    } else if(e=='parsererror') {
		        alert('Error.\nParsing JSON Request failed.');
		    } else if(e=='timeout'){
		        alert('Request Time out.');
		    } else {
		        alert('Unknow Error.\n'+x.responseText);
		    }
			}

			function insert_control_panel(){
				// check Temperature button
				var txt = '<input type="button" id="T_check_but" value="Check Temp"  class="ctrl_button" title="Check current temperature.">';
				$("#T_check").html(txt);
				$("#T_check_but").click(function(){

					$.ajax({
						type: "POST",
						//dataType: "json",
						url: "./T_check.php",
						success: function( data ) {
							T_check_id = data;
							console.log("T_check_id: " + T_check_id);
							setTimeout(function(){get_T();}, 500);
							// console.log(data);
							// var txt = data.Temperature + " &deg;C";
							// $( "#T_check_output" ).html( txt );
						},
						error: function(x, e) {
							ajax_error(x,e);
						}
					});


				});

				// turn on crockpot button
				var txt = '<input type="button" id="runCrock_but" class="ctrl_button" value="Start Pot">';
				$("#runCrock").html(txt);

				//set to on or off based on current status
				set_Crockpot_button();

				$("#runCrock").click(function(){
					upData = {on: l_on ? 0: 1};
					$.ajax({
						type: "POST",
						//dataType: "json",
						url: "./runCrock.php",
						data: upData,
						success: function( data ) {
							//switch l_on
							//l_on = l_on === true ? false : true;
							set_Crockpot_button();
							// console.log("starting crockpot: "+l_on);
							// console.log(JSON.stringify(data));
							// if (l_on){
							// 	$("#runCrock_but").val("Stop Crockpot");
							// } else {
							// 	$("#runCrock_but").val( "Start Crockpot");
							// }

						},
						error: function(x, e) {
							ajax_error(x,e);
						}
					});



				});
			}

			function set_T(){

				var Tp = prompt("Enter new Set Temperature (&deg;C):");
				var T = parseFloat(Tp);
				var Tmax = 100.0;
				var Tmin = 10.0;
				if ($.isNumeric(T)){
					if ((T > Tmin) && (T < Tmax)){
						//update the temperature using this Value
						upData = {
							parameter: 'set_T',
							value: T,
						};
						$.ajax({
							type: "POST",
							//dataType: "json",
							url: "./web_com.php",
							data: upData,
							success: function( data ) {
								console.log(JSON.stringify(data));
								$("#set_T").html(JSON.stringify(data));
								get_settings();
							},
							error: function(x, e) {
								ajax_error(x,e);
							}
						});
					} else {
						alert("Temperature out of range: Max: "+Tmax+" | Min: " +Tmin);
					}


				} else {
					alert("Not a number:"+Tp);
				}

			}

			function set_web_com_parameter(parameter, value){
				upData = {
					parameter: parameter,
					value: value,
				};
				$.ajax({
					type: "POST",
					//dataType: "json",
					url: "./web_com.php",
					data: upData,
					success: function( data ) {
						console.log(JSON.stringify(data));
						get_settings();
					},
					error: function(x, e) {
						ajax_error(x,e);
					}
				});
			}


			function set_K(parameter, value){
				var id = parameter;

				var K = typeof val === 'undefined' ? $("#"+id+"_in").val() : parseFloat(value);

				if ($.isNumeric(K)){
					upData = {
						parameter: id,
						value: K,
					};
					$.ajax({
						type: "POST",
						//dataType: "json",
						url: "./web_com.php",
						data: upData,
						success: function( data ) {
							console.log(JSON.stringify(data));
							//$("#"+id+"_in").val(JSON.stringify(data));
							//$("#set_T").html(JSON.stringify(data));
							get_settings();
						},
						error: function(x, e) {
							ajax_error(x,e);
						}
					});

				} else {
					alert("Not a number:"+Tp);
				}

			}
