from application import application_run

app = application_run()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8081)
