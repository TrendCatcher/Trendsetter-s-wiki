---
title: "[MVC 프레임워크]FrontController -V1"
date: 2025-04-03 06:12:12
url_slug: "MVC-프레임워크FrontController"
---

![](https://velog.velcdn.com/images/trendsetter/post/f0f1b6b6-890c-456f-8075-bfc7ad7cb666/image.png)
![](https://velog.velcdn.com/images/trendsetter/post/ceaa6ba3-10f6-4bfa-84c1-e10ad42ab8e7/image.png)
FrontConroler 패턴 특징
위의 두그림의 비교에서 보이는 것과 같이 프런트 컨트롤러는 하나의 클라이언트의 요청을 받는다. 프런트 컨트롤러가 요청에 맞는 컨트롤러를 찾아서 호출하여 **입구를 하나로** 컨트롤러들의 공통 기능을 처리할 수 있다.

### 스프링 웹 MVC와 프런트컨트롤러
스프링 웹 MVC의 핵심도 바로 FrontController이며 DispatcherServlet이 FrontController패턴으로 구현이 되어있다. 다만, 단계적으로 FrontController를 도입하여 구현이유를 명확히 한다.

## 프론트 컨트롤러 도입 - v1
첫단계는 기존 코드를 최대한 유지하면서, FrontController를 도입하는 것이다. 먼구 구조를 소개한다. 
![](https://velog.velcdn.com/images/trendsetter/post/9317c83f-cd16-4336-860e-8853010af228/image.png)
```java
public interface ControllerV1{
	void process(HttpServletRequest request, HttpServletResponse response)throws ServletException, IOException;
}
```

다음과 같이 서블릿과 비슷한 모양의 컨트롤러 인터페이스를 도입한다.
각 컨트롤러들은 이 인터페이스를 구현하기만 하면 된다.
FrontController는 이 인터페이스를 호출해서 구현과 관계없이 **일관성**을 가질 수 있다. 
이제 이 인터페이스를 구현한 컨드롤러를 만든다. 핵심은 기존 로직을 최대한 유지하는 것이다. 

MemberFormControllerV1 - 회원 등록 컨트롤러
```java
public class MemberFormControllerV1 implements ControllerV1{
	@Override
     public void process(HttpServletRequest request, HttpServletResponse 
response) throws ServletException, IOException{
	String viewPath = "WEB-INF/views/new-form.jsp";
    RequestDispatcher dispatcher = request.getReqeustDispatcher(viewPath);
    dispatcher.forward(request,response);
	}
}
```

MemberSaveControllerV1 - 회원저장 컨트롤러
```java
public class MemberSaveControllerV1 implements ControllerV1{

	private MemberRepository memberRepository = MemberRepository.getInstance();
	
    public void process(HttpServletRequest request, HttpServletResponse 
response) throws ServletException, IOException {
	String username = request.getParameter("usename");
    int age = Integer.parseInt(request.getParameter("age"));
    
    Member member = new Member(username, age);
    memberRepository.save(member);
    
    request.setAttribute("member",member);
    // servlet에서 생성한 객체를 JSP로 전달함으로써 Model에 데이터를 보관함
    //[중요!!]컨트롤러(서블릿)와 뷰(JSP)를 분리하는 중요한 역할
    
    String viewPath = "/WEB-INF/views/save-result.jsp";
    RequestDispatcher dispatcher = request.getRequestDispatcher(viewPath);
    dispatcher.forward(reqeust,response);
	}
}
```
MemberListControllerV1 - 회원 목록 컨트롤러
```java
public class MemberListControllerV1 implements ControllerV1{
	 @Override
 	public void process(HttpServletRequest request, HttpServletResponse 
response) throws ServletException, IOException{
	List<Member> members = memberRepository.findAll();
    request.setAttribute("members",members);
    
    String viewPath = "/WEB-INF/views/members.jsp";
    RequestDispathcer dispatcher = request.getRequestDispatcher(viewPath);
    dispatcher.forward(request,response);
	}
}
```
내부 로직은 기존 서블릿과 같다. 
이제 프론트 컨트롤러를 만든다.

```java
@Webservlet(name="frontControllerServletV1", urlPatterns="front-controller/v1/*")
public class FrontControllerServletV1 extends HTTPServlet{
	private Map<String, ControllerV1> controllerMap = newHahsMap<>();
    
    //1. 매핑정보를 넣는다.
    public FrontControllerServletV1(){//constructor
    	controllerMap.put("/front-controller/v1/members/new-form", new MemberFormControllerV1());
        controllerMap.put("/front-controller/v1/members/save", new MemberSaveControllerV1());
        controllerMap.put("/front-controller/v1/members", new MemberListControllerV1());
    }
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse 
response) throws ServletException, IOException{

		 System.out.println("FrontControllerServletV1.service");
         String requestURI = request.getRequestURI();
         ControllerV1 controller = controllerMap.get(requestURI);
         
         if(controller == null){
         response.setStatus(HTTPServeltResponse.SC_NOT_FOUND);
         return;
         }
         controller.process(request,response);
	}
}
```

자 이제 주요 code snippet들을 뜯어보면서 프런트 컨트롤러를 분석한다. 

### urlPatterns
- urlPatterns="/front-controller/v1/*" : /front-controller/v1의 모든 하위 요청은 이 서블릿에서 받아들인다.
- 예시)  
/front-controller/v1, /front-controller/v1/a, /front-controller/v1/a/b

### controllerMap
- key: 매핑 URL
- value: 호출될 컨트롤러

### service()
먼저 requestURI()를 조회해서 실제 호출할 컨트롤러를 controllerMap에서 찾고 만약 없으면 404반환.
컨트롤러 찾고 controller.process()호출해서 해당 컨트롤러 실행

## 궁금했던 점
> 1. FrontController VS FrontControllerServlet

``` FrontController``` 는 인터페이스로 만들어진 "기능의 틀"이다. 
반면, ```FrontControllerServlet```은 실제 구현체라고 보면 된다. 

좀더 자세히 보자. ```**FrontController**```는 "모든 요청을 하나의 진입점에서 받아 처리"하기 위해 기본 규약을 정리한 것이다. 
-> **일관성**을 가진다!

반면, ```**FrontControllerServlet**```은 보통 ```HTTPServlet```을 상속받는 구현체로, 실제로 웹 어플리케이션에서 **실제 요청을 받아 처리**하는 부분이다. 
