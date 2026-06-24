---
title: "HTTP protocol Spec"
date: 2024-07-09 03:40:59
url_slug: "HTTP-protocol-Spec"
---

> http protocol은 클라이언트와 서버 간에 데에터 교환을 하기 위한 표준 프로토콜이다. request와 response는 http protocol의 핵심 요소이며 각각의 메세지는 다음과 같은 구조로 이루어진다. 

# HTTP request 메시지 구조
 클라이언트가 서버로 요정하는 메시지이며 다음과 같은 구조이다. 
 
##  1. Start Line:
- HTTP 메소드
	1. **GET**: data를 서버로부터 요청할 때 사용, 
    	- URL에 데이터를 붙여서 전송, 메시지 바디 없이 **query string형태**로 **URL 끝에 '?' 뒤에 키-값 쌍을 사용해 데이터를 전달**
        - 캐시 가능하며, 브라우저 히스토리에 기록될 수 있다. 
        - 보안적으로 민감한 데이터는 GET 메소드를 통해 전송하는 것이 좋지 않다. 
        - 예) 검색, 필터, 페이징 툴에서 많이 사용

2.  **POST(HTML Form)**: 서버에 데이터를 전송할 때 사용
    	- HTTP 메시지의 본문에 데이터를 담아서 전송, GET 메소드보다 많은 양의 데이터를 전송할 수 있다. username=hello&age=20
        - 보안적으로 GET메소드보다 더 안전하게 데이터를 전송
        - 캐시 기능 지원하지 않음
- URL(요정하는 리소스의 경로)
- HTTP version(ex: HTTP/1.1)

```
GET /index.html HTTP/1.1
```
3. **HTML message body**에 데이터를 직접 담아서 요청
	- HTTP API에 주로 사용, Json, XML, TEXT
    - 데이터 형식은 주로 JSON사용
    
## 2. Header Fields
> 요청에 대한 추가 정보를 다룬다.
- Content-Length
- Content-Type
- Set-Cookie
- Location
위와 같은 요소들이 포함될 수 있으며, 이를 통해 **요청과 응답**의 **성격**, **데이터 형식**,**인코딩 방식**등을 특정할 수 있다.
```
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Content-Type: application/json
```

## 3. 빈 줄
헤더와 본문 사이에 빈줄이 필수적이다.

## 4. Message Body(본문)
POST 요청과 같이 본문(body)에 데이터가 포함될 수 있다.
```
{
  "username": "johndoe",
  "password": "secretpassword"
}

```
GET요청의 경우 일반적으로 본문이 비어있음을 나타내는 빈 줄만 있다. 

# 요약
HTTP 프로토콜의 request와 response 메시지는 
1. **HTTP메소드(GET,POST등)**, **url**, **HTTP 버젼**으로 이루어진 시작라인 
2. 헤더필드(client <-> server 간 통신에 대한 메타데이터를 전달) 
3. 빈줄
4. 메시지 바디
로 이루어져 있다. 
이러한 구성형식은 client와 server간의 데이터 교환, 웹페이지의 내용 표시, 동적데이터의 처리를 원할하게 한다. 
