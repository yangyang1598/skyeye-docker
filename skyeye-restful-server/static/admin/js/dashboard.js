let create_chart_module = (function($) {
    let Module = {
        init: function(opts) {
            // django 템플릿 부분
            const date = opts.date
            const chartData1 = opts.temperature;
            const chartData_roll = opts.camera_roll;
            const chartData_pitch = opts.camera_pitch;
            const chartData_yaw = opts.camera_yaw;
            const chartData2 = opts.date2;
            const arr_get_serial = opts.site_name;

            const DateTime = luxon.DateTime;
            // 받아온 date 데이터 날짜 계산 => luxon
            // https://moment.github.io/luxon/index.html

            const CREATE_YEAR = 1, CREATE_MONTH = 3, CREATE_DAY = 4;
            const DEFAULT_OPTION = arr_get_serial[1]["site_id"];
            let save_query = "";
            let query_result = get_query();
            let query_length = Object.keys(query_result).length;
            //  console.log(save_query);
            //  console.log(query_result);
            //  console.log(query_length);

            // URL의 파라미터를 받아온다 => {date__month: '3', date__year: '2023'}
            function get_query() {
                var url = document.location.href;
                var qs = url.substring(url.indexOf('?') + 1).split('&');
                let query_string = url.split('?')[1];
                if (query_string != "") {
                    save_query = "?" + url.split('?')[1];
                }
                for(var i = 0, query_result = {}; i < qs.length; i++){
                    qs[i] = qs[i].split('=');
                    query_result[qs[i][0]] = decodeURIComponent(qs[i][1]);
                }
                return query_result;
            }

            // 임무장비 차트 데이터 리스트
            let date_list = [];

            function get_date_list(d) {
                date_list.push(d.day.split('-')[2].substr(0, 2));
                date_list = [...new Set(date_list)].sort(); // 중복 제거 및 순서대로 정렬
            }

            // 임무장비 차트
            const ctx = document.getElementById('myChart1');
            chartData1.forEach((d) => {
                d.x = new Date(d.day);
                get_date_list(d);
                // console.log(d)
            });

            const chart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        datasets: [
                            {
                                label: "temperature",
                                data: chartData1,
                                fill: false,
                                backgroundColor: 'rgba(33,150,243,0.5)',
                                // yAxisID: 'y',
                            },
                        ],
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    displayFormats: {
                                        day: 'MMM dd'
                                    }
                                },
                                ticks: {
                                    // stepSize: 15,
                                }
                            },
                            y: {
                                ticks: {
                                    // ⑬시작을 0부터 하게끔 설정(최소값이 0보다 크더라도)(boolean)
                                    beginAtZero: false,
                                },
                            },
                        }
                    }
                });

            if (query_length >= CREATE_DAY) {
                chart.options.scales.x.time = {
                    unit: 'minute',
                    displayFormats: {
                        minute: 'h:mm: a'
                    }
                };
                chart.update();
            } // 임무장비 차트 끝

            // 카메라 차트
            const ctx3 = document.getElementById('myChart3').getContext('2d');

            // Sample data

            chartData_roll.forEach((d) => {
                d.x = new Date(d.day);
                // console.log(d)
            });
            chartData_pitch.forEach((d) => {
                d.x = new Date(d.day);
                // console.log(d)
            });
            chartData_yaw.forEach((d) => {
                d.x = new Date(d.day);
                // console.log(d)
            });
            // Render the chart
            const chart3 = new Chart(ctx3, {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: "camera_roll",
                            data: chartData_roll,
                            fill: false,
                            backgroundColor: 'rgba(255,0,0,0.5)',
                            // yAxisID: 'y',
                        },
                        {
                            label: "camera_pitch",
                            data: chartData_pitch,
                            fill: false,
                            backgroundColor: 'rgba(0,255,0,0.5)',
                            // yAxisID: 'y',
                        },
                        {
                            label: "camera_yaw",
                            data: chartData_yaw,
                            fill: false,
                            backgroundColor: 'rgba(0,0,255,0.5)',
                            // yAxisID: 'y',
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                // unit: 'second',
                                // round: 'seconds',
                                // tooltipFormat: 'h:mm:ss a',
                                displayFormats: {
                                    hour: 'h a',
                                    minute: 'h:mm a',
                                    second: 'h:mm:ss a',
                                    // second: 'MMM D, h:mm:ss a',
                                    // round: 'MMM D, h:mm:ss a'
                                },
                            },
                        },
                        y: {
                            min: 0,
                            max: 1500,
                            ticks: {
                                // ⑬시작을 0부터 하게끔 설정(최소값이 0보다 크더라도)(boolean)
                                beginAtZero: false,
                                stepSize: 100,
                            },
                        },
                    },
                },
            }); // 카메라 차트 끝

            // 윈치 차트
            const ctx2 = document.getElementById('myChart2').getContext('2d');

            // Sample data

            chartData2.forEach((d) => {
                d.x = new Date(d.day);
                // console.log(d)
            });

            // Render the chart
            const chart2 = new Chart(ctx2, {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: "tetherline_angle",
                            data: chartData2,
                            fill: false,
                            backgroundColor: 'rgba(33,150,243,0.5)',
                        },
                    ],
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                displayFormats: {
                                    hour: 'h a',
                                    minute: 'h:mm a',
                                    second: 'h:mm:ss a',
                                    // second: 'MMM D, h:mm:ss a',
                                },
                            },
                        },
                        y: {
                            ticks: {
                                // ⑬시작을 0부터 하게끔 설정(최소값이 0보다 크더라도)(boolean)
                                beginAtZero: false,
                            },
                        },
                    },
                },
            }); // 윈치 차트 끝

            // URL에서 특정 이름의 파라미터 빼내는 함수
            $.urlParam = function(name) {
                var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(location.href);
                if (results==null) {
                    return null;
                } else {
                    return results[1] || 0;
                }
            }

            // site_name 셀렉트 박스에 가져온 임무장비 갯수만큼 추가
            for (let i = 0; i < Object.keys(arr_get_serial).length; i++) {
                // console.log(arr_get_serial[i]);
                $("#site_name").append('<option value="' + arr_get_serial[i]["site_id"] + '">' + arr_get_serial[i]["name"] + '</option>');
            }

            // 대시보드 임무장비 변경할 때 해당 임무장비 경로로 리다이렉트 (?options=임무장비명)
            let site_name = "";
            $("#site_name").change(function() {
                // console.log($(this).val());
                let site_name = $(this).val();
                // $("#prev_date").attr("href", "?options=" + site_name);
                // $(".added_button")
                location.href = `?options=${site_name}`;
            });

            // URL 쿼리 스트링에서 ?options 값 가져오기
            const OPTION_PARAMETER = $.urlParam('options');
            let options = "";
            // URL에 options가 없으면 test1 선택 / 있으면 선택내역 저장
            if (OPTION_PARAMETER == null) {
                options = DEFAULT_OPTION;
                $("#site_name").val(DEFAULT_OPTION).attr('selected', true);
            } else {
                options = OPTION_PARAMETER;
                $("#site_name").val(OPTION_PARAMETER).attr('selected', true);
            }
            // console.log(options);

            // 날짜 계산 => 연/월/일 분리
            const month_name = ["January","February","March","April","May","June","July","August","September","October","November","December"];
            let first_iso_time = DateTime.fromISO(date[0]);
            let second_iso_time = DateTime.fromISO(date[1]);

            let current_year = first_iso_time.year;
            let current_month = first_iso_time.month;
            let current_day = first_iso_time.day;
            // let current_hour = first_iso_time.hours;

            // 버튼 생성 함수의 반복분 몇회 반복할 지 설정
            let last_month = second_iso_time.month;
            // let last_day = second_iso_time.day;

            // 버튼 생성 함수
            function create_button(check_key) {
                switch (check_key) {
                    case CREATE_YEAR: // 연 버튼
                        for (let i = 0; i < last_month; i++) {
                            const month_button = '<a href="?options=' + options + '&amp;date__month=' + (i+1) + '&amp;date__year=' + current_year
                                                + '" class="added_button btn btn-primary ml-1 my-1">' + month_name[i] + "&nbsp;" + current_year + '</a>';
                            $(".date-hierarchy").append(month_button);
                        };
                        break;
                    case CREATE_MONTH: // 월 버튼
                        // console.log(date_list); // [10, 11, 12 ...] => 임무장비 데이터가 존재하는 날짜만큼 반복
                        for (let i = 0; i < date_list.length; i++) {
                            const date_button = '<a href="?options=' + options + '&amp;date__day=' + date_list[i] + '&amp;date__month=' + current_month + '&amp;date__year=' + current_year
                                                + '" class="added_button btn btn-primary ml-1 my-1">' + month_name[current_month-1] + "&nbsp;" + date_list[i] + '</a>';
                            $(".date-hierarchy").append(date_button);
                        };
                        break;
                    case CREATE_DAY: // 일 버튼
                        const current_date_button = '<button class="added_button btn btn-primary ml-1 my-1">'
                                                    + month_name[current_month-1] + '&nbsp;' + current_day + '</button>';
                        $(".date-hierarchy").append(current_date_button);
                        break;
                }
            }; // create_button

            // URL 쿼리 길이에 따라 버튼 생성
            switch (query_length) {
                case 1:
                    // console.log("All dates 표시함");
                    $("#prev_date").text("\u2039 All dates")
                    .attr("href", "?options=" + options);
                    create_button(CREATE_YEAR);
                    break;
                case 3:
                    // console.log("2023 표시함");
                    $("#prev_date").text("\u2039 " + current_year)
                    .attr("href", "?options=" + options);
                    create_button(CREATE_MONTH);
                    break;
                default:
                    $("#prev_date").text("\u2039 " + month_name[current_month - 1] + "\u0020" + current_year)
                    .attr("href", "?options=" + options + "&date__month=" + current_month + "&date__year=" + current_year);
                    create_button(CREATE_DAY);
                    add_time_picker_button();

                    // 시간 필터 추가
                    $("#timepicker").show();

                    // form에 URL 파라미터 저장용 hidden 속성 추가
                    $(".save-option").val(options);
                    $(".save-day").val(current_day);
                    $(".save-month").val(current_month);
                    $(".save-year").val(current_year);
                    break;
            } // switch

            // 타임피커 생성 함수
            function add_time_picker_button() {
                // Timepicker 추가
                // https://github.com/pglejzer/timepicker-ui
                const first_dom = document.querySelector(".timepicker-ui-1");
                const second_dom = document.querySelector(".timepicker-ui-2");
                let time_options = {};
                
                // 시간 선택한 적이 없으면 현재 시간 입력
                if (query_length != 6) {
                    time_options = { currentTime: { time: new Date(), updateInput: true, locales: "en-US", preventClockType: false } };
                } else { 
                    // 시간 선택했었으면 선택한 시간 값 저장\
                    time_picker_save();
                }
                const first_picker = new window.tui.TimepickerUI(first_dom, time_options);
                const second_picker = new window.tui.TimepickerUI(second_dom, time_options);
                first_picker.create();
                second_picker.create();

                if (query_length != 5) {
                    // 현재 시간에서 1시간 빼기
                    let minus_time = DateTime.now().minus({hours:1}).toFormat('hh:mm a');
                    $("#first_timepicker").val(minus_time);
                }
            }; // add_time_picker_button

            // 타임피커 시간 저장 함수
            function time_picker_save() {
                let convert_time_1 = query_result.date__range__gte_1.split(':');
                let convert_time_2 = query_result.date__range__lte_1.split(':');
                convert_time_1 = DateTime.now().set({hours:convert_time_1[0], minutes:convert_time_1[1]}).toFormat('hh:mm a');
                convert_time_2 = DateTime.now().set({hours:convert_time_2[0], minutes:convert_time_2[1]}).toFormat('hh:mm a');
                $("#first_timepicker").val(convert_time_1);
                $("#second_timepicker").val(convert_time_2);
            } // time_picker_save

            // 타임피커 시간 체크 함수
            function time_picker_check() {
                if ($("#first_timepicker").val() == "" || $("#second_timepicker").val() == "") return false;
                const HOUR = 0;
                const MINUTE = 1;
                let get_first_time = $("#first_timepicker").val().split(':');
                let get_second_time = $("#second_timepicker").val().split(':');
                let get_first_12hour = get_first_time[1].split(' ')[1];
                let get_second_12hour = get_second_time[1].split(' ')[1];
                let temp_hour;

                // 시분 변환
                get_first_time = DateTime.now().set({hours:get_first_time[HOUR], minutes:get_first_time[MINUTE].substr(0,2)}).toFormat('hh:mm');
                get_second_time = DateTime.now().set({hours:get_second_time[HOUR], minutes:get_second_time[MINUTE].substr(0,2)}).toFormat('hh:mm');

                // PM이면 12시간 더함
                if (get_first_12hour == 'PM') {
                    get_first_time = get_first_time.split(':');
                    temp_hour = parseInt(get_first_time[HOUR]);
                    if (temp_hour == 12) {
                        get_first_time = `${temp_hour}:${get_first_time[MINUTE]}`;
                    } else {
                        get_first_time = `${temp_hour + 12}:${get_first_time[MINUTE]}`;
                    }
                }
                if (get_second_12hour == 'PM') {
                    get_second_time = get_second_time.split(':');
                    temp_hour = parseInt(get_second_time[HOUR]);
                    if (temp_hour == 12) {
                        get_second_time = `${temp_hour}:${get_second_time[MINUTE]}`;
                    } else {
                        get_second_time = `${temp_hour + 12}:${get_second_time[MINUTE]}`;
                    }
                }

                // [시, 분] 배열로 변환
                let get_first_time_array = get_first_time.split(':');
                let get_second_time_array = get_second_time.split(':');

                if (get_first_time_array[HOUR] >= get_second_time_array[HOUR]) {
                    if (get_first_time_array[MINUTE] >= get_second_time_array[MINUTE]) {
                        return false;
                    } else {
                        $("#first_timepicker").val(`${get_first_time}`);
                        $("#second_timepicker").val(`${get_second_time}`);
                        return true;
                    }
                } else {
                    $("#first_timepicker").val(`${get_first_time}`);
                    $("#second_timepicker").val(`${get_second_time}`);
                    return true;
                }
            }; // time_picker_check

            // 타임피커 Search 버튼 submit 이벤트
            $("#time_range_search").submit(function(e) {
                // e.preventDefault();
                let submit_result = time_picker_check();
                if (submit_result == false) {
                    e.preventDefault();
                    alert("select correct time");
                }
            }); // submit
        }
    };

    return Module;
  })(jQuery);