```
FROM tomcat:8.5-jdk8-openjdk
COPY ./elegant-love.jsp /usr/local/tomcat/webapps/ROOT/elegant-love.jsp
```
> Dockerfile

```bash
sudo docker build -t my-tomcat-app .
sudo docker run -it --rm -p 8888:8080 my-tomcat-app
```

http://localhost:8888/elegant-love.jsp
```javascript
document.cookie='LOVE=your_cookie_value'
```
