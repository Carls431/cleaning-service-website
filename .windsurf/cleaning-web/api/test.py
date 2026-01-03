def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': '<h1>Hello from Vercel!</h1><p>Your Flask app is working!</p>'
    }
