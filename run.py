""" To launch flaskr """
import sys
import flaskr


if __name__ == "__main__":
    """ set app config """
    options = flaskr.get_options_from_command_line(args=sys.argv)
    flaskr.app.config.update(ENV=options["env"], TESTING=options["testing"], DEBUG=options["debug"])
    """ launch server """
    if options["env"] == "development":
        flaskr.app.run(host='0.0.0.0', port=5000)
    else:
        from waitress import serve
        serve(flaskr.app, host="0.0.0.0", port=5000)
