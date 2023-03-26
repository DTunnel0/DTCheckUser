page = '''<!DOCTYPE HTML>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CHECKUSER</title>

    <style>
        @import url(https://fonts.googleapis.com/css?family=Roboto:400,300,100,500,700,900);

        html,
        body {
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #2c2d30 0%, #353535 100%);
            width: 100%;
            height: 100vh;
        }

        .container {
            margin: 1rem;
            border-radius: 50px;
            border: none;
            background: rgb(39, 39, 39);
            width: 300px;
            padding: 30px;
        }

        .container h1 {
            color: white;
            font-size: 1.5rem;
            margin-bottom: 20px;
        }

        .container h4 {
            color: white;
            font-size: 1rem;
            margin-bottom: 20px;
        }

        .container h4 span {
            background: #363636;
            padding: 5px;
            border-radius: 50px;
            font-size: 0.8rem;
        }
    </style>

</head>

<body>
    <div class="container">
        <h1>CHECKUSER - @DuTra01</h1>
        <h4>TOTAL DE CONEXÕES: <span id="total">00</span></h4>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.1.min.js"
        integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>
    <script src="https://cdn.socket.io/4.5.3/socket.io.min.js"
        integrity="sha384-WPFUvHkB1aHA5TDSZi6xtDgkF0wXJcIIxXhC6h8OT8EH3fC5PWro5pWJ1THjcfEi"
        crossorigin="anonymous"></script>
    <script type="text/javascript" charset="utf-8">
        $(document).ready(function () {
            const socket = io();
            socket.on('message', function (data) {
                data = JSON.parse(data);
                if (data.total != undefined) {
                    $('#total').text(String(data.total).padStart(2, '0'));
                }
            });

            socket.emit('message', {
                action: 'all',
                data: null
            });
        });
    </script>
</body>

</html>
'''
