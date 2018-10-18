import ubike


if __name__ == '__main__':
    app = ubike.create_app()
    app.run(debug=True)