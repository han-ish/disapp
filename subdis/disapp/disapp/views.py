from django.http import HttpResponse

def index(request):
	html = """<html>
			<head>
			<title>Index</title>
			<script type="text/javascript">
				function to_disapp(){
					window.location="/qa/signin/";
				}
			</script>
			</head>
			<body onload="to_disapp();">Nothing to see here</body>
		</html>"""
	return HttpResponse(html)
