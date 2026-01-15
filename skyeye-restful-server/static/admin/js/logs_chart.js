var create_table_module = (function($) {
    var Module = {
        init: function(opts) {
            let arr_get_serial = opts.serial_number;
            const chartData = opts.date;
            let label_text = opts.label_text;

            const DateTime = luxon.DateTime;
            const DATE = 0, TIME = 1;

            let save_query = [];
            let serial_number = "";
            let options = "";

            // URL에서 파라미터를 뽑아서 save_query 배열에 push
            const searchParams = new URLSearchParams(location.search);
            for (const param of searchParams) {
                save_query.push(param);
            }

            // serial_number 셀렉트 박스에 가져온 임무장비 갯수만큼 추가

            for (let i = 0; i < Object.keys(arr_get_serial).length; i++) {
                $("#serial_number").append('<option value="' + arr_get_serial[i].serial_number + '">' + arr_get_serial[i].serial_number + '</option>');
            }

            // 오늘 날짜 => 연도 요일 / 현재 시간으로 분리 || 현재시간 - 1시간 빼기 
            let today = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss').split(' ');
            let minus_time = DateTime.now().minus({hours:1}).toFormat('HH:mm:ss');

            // URL에 파라미터가 1개 이상이라면 파라미터에서 str 추출해서 셀렉트 박스 및 input에 집어넣음
            if (save_query.length > 0) {
                $("#serial_number").val(save_query[0][1]).attr("selected", true);
                $("#options").val(save_query[1][1]).attr("selected", true);
                $("#start_date").val(save_query[2][1]);
                $("#start_time").val(save_query[3][1]);
                $("#end_date").val(save_query[4][1]);
                $("#end_time").val(save_query[5][1]);
                serial_number = save_query[0][1];
                options = save_query[1][1];
            } else { // 파라미터가 없다면 현재시간 집어넣음
                $("#start_date").val(today[DATE]);
                $("#start_time").val(minus_time);
                $("#end_date").val(today[DATE]);
                $("#end_time").val(today[TIME]);
            }

            $(".select_today").click(function(e) {
                e.preventDefault();
                $(this).prev().val(today[DATE]);
            });

            $(".select_now").click(function(e) {
                e.preventDefault();
                $(this).prev().val(today[TIME]);
            });

            $("#serial_number").change(function() {
                serial_number = $(this).val();
            });
            
            $("#options").change(function() {
                options = $(this).val();
            });
            
            // Search 버튼 눌렀을 때 시리얼과 옵션 선택 여부 체크
            $("#btn_submit").click(function() {
                if (options == "" || serial_number == "") {
                    alert("Check your select");
                } else {
                    $("#changelist-search").submit();
                }
            });
            
            // Reset 버튼 누르면 아래 지정된 시간으로 초기화
            $("#btn_reset").click(function() {
                let reset_date = '2023-02-27';
                let reset_time = DateTime.now().set({hours: 11, minutes: 0, seconds: 0});
                $("#start_date").attr('value', reset_date);
                $("#start_time").attr('value', reset_time.minus({hours: 1}).toFormat('HH:mm:ss'));
                $("#end_date").attr('value', reset_date);
                $("#end_time").attr('value', reset_time.toFormat('HH:mm:ss'));
            });

            /// 차트 부분
            // =====================================================================================
            // 차트 라벨 바꾸기
            // URL에서 특정 이름의 파라미터 빼내는 함수
            $.urlParam = function(name) {
                var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
                if (results==null) {
                    return null;
                } else {
                    return results[1] || 0;
                }
            }

            // URL에 options 파라미터가 있다면 차트 라벨 변경
            if ($.urlParam('options') != null) label_text = $.urlParam('options');
            // =====================================================================================

            const ctx = document.getElementById('myChart').getContext('2d');
            // Sample data

            // console.log(chartData);
            // const chartData = JSON.parse(document.getElementById("chart-data").textContent);
            // const chartKey = JSON.parse(document.getElementById("chart-key").textContent);
            // const chartValue = JSON.parse(document.getElementById("chart-values").textContent);

            // console.log(chartData);

            // Parse the dates to JS
            // Object.keys(chartData).forEach(d => {
            //     d.x = new Date(d.date);
            //     console.log(d)
            // });

            chartData.forEach((d) => {
                d.x = new Date(d.hour);
                // console.log(d)
            });

            // Render the chart
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [
                        { 
                        label: label_text,
                        data: chartData,
                        fill: false,
                        backgroundColor: 'rgba(33,150,243,0.5)',
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        x:  {
                            type: 'time',
                            time: {
                                displayFormats: {
                                    hour: 'h a',
                                    minute: 'h:mm a',
                                    second: 'h:mm:ss a',
                                },
                            },
                        },
                        y:  {
                            ticks: {
                                // ⑬시작을 0부터 하게끔 설정(최소값이 0보다 크더라도)(boolean)
                                beginAtZero: false,
                            },
                        },
                    },
                },
            });
        },
    };
  
    return Module;
  })(jQuery);