import network
wlan_sta=network.WLAN(network.STA_IF)


codeboot = ''

def wifi_manager():
    ssids=sorted(ssid.decode('utf-8') for ssid,*_ in wlan_sta.scan())
    html = """\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """

    while len(ssids):
        ssid=ssids.pop(0)
        html += """\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid)
    html += """\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h2 style="color: #2e6c80;">
                Some useful infos:
            </h2>
            <ul>
                <li>
                    Original code from <a href="https://github.com/cpopp/MicroPythonSamples"
                        target="_blank" rel="noopener">cpopp/MicroPythonSamples</a>.
                </li>
                <li>
                    This code available at <a href="https://github.com/tayfunulu/WiFiManager"
                        target="_blank" rel="noopener">tayfunulu/WiFiManager</a>.
                </li>
            </ul>
        </html>
    """
    return html

wifi_manager_success = """\
            <html>
                <center>
                    <br><br>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP successfully connected to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                </center>
            </html>
        """

wifi_manager_error = """\
            <html>
                <center>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """