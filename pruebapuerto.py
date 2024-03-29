import dash

app = dash.Dash(__name__)

# Agregar el código de la aplicación aquí

if __name__ == '__main__':
    app.run_server(debug=True)
    print('El servidor está ejecutándose en el puerto:', app.server.port)

#http://127.0.0.1:8050/