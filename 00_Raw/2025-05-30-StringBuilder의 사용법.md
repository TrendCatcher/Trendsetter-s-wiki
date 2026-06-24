---
title: "StringBuilder의 사용법"
date: 2025-05-30 04:13:27
url_slug: "StringBuilder의-사용법"
---

> 포스팅 이유

문자나 문자열을 뒤집는 것은 상당히 많이 쓰이고 중요한 기본기이다. 풀이를 하면서 StringBuilder의 역할과 내부 동작 원리를 정리하고자 본 포스팅을 하게 되었다. 

백준의 9093번 문제이다. 

https://www.acmicpc.net/problem/9093

공백단위로 나뉘어진 문장을 단어별로 나누어 뒤집고 출력하는 단순한 문제로 브론즈 1수준이다. 

>풀이 흐름

1. TestCase를 입력 받고, 
2. 해당 TC가 실행 될 동안 문장을 계속 입력받은 후,
3. 문장을 공백 단위로 쪼개 배열안에 저장한 다음,
4. StringBuilder를 활용하여 각 배열의 요소를 뒤집어 출력한다.

```java
class boj_9093{
    static String[] arr;
    public static void main(String[]args)throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        StringBuilder sb = new StringBuilder();

        while(N-->0){
            String cmd = br.readLine();
            arr = cmd.trim().split(" ");    //convert sentence cmd to array in blank units

            for(int i=0;i<arr.length;i++) {
                sb.append(new StringBuilder(arr[i]).reverse());
                sb.append(" ");
            }
            sb.append("\n");

        }

        System.out.println(sb);
    }
}
```

해당 코드를 짜면서 몇가지 의아한 질문을 던지게 되었다. 



### ❓질문
#### 1. reverse()는 객체를 반환하는데 
sb.append(new StringBuilder(cmd).reverse());에 toString()이 필요하지 않은 이유? 

-> 분명 코드를 짤때는 intelliJ에서 오류 메세지가 뜨지 않았다. 그렇다면 StringBuilder클래스의 toString()메서드가 .append()에서 자동으로 호출되는 것인가 라는 질문으로 이어진다. 

결론은 O.


🔍 StringBuilder.append(Object obj)의 정의

```java
public StringBuilder append(Object obj){
	return append(String.valueOf(obj));
}
```
즉 반환형은 String.valueOf(obj)인데, 이 메서드는 내부적으로 obj.toString()을 호출한다. 

🔁 코드 흐름 분석

```java
sb.append(new StringBuilder(arr[i]).reverse());
```

1. arr[i]는 String을 기반으로 새로운 StringBuilder 객체를 생성한다.
2. .reverse()를 호출하여 StringBuilder 객체 자체를 반환한다.
3. sp.append()에서 Object타입으로 StringBuilder에 전달한다.
4. 내부적으로 toString()이 호출된다.
5. 결국 sb.append()는 문자열로 반환된 뒤집힌(reversed)값을 추가한다. 

>정리

결국 StringBuilder를 사용하면 append()메소드 내무에서 자동으로 toString()을 호출한다!

### [꼬리질문] 매번 new 를 통해 새로운 StringBuilder 를 생성하는 이유??

각 단어는 그대로 두되, **각 단어 내부의 문자 순서만 뒤집는 것**이 핵심이다.
```java
for (int i = 0; i < arr.length; i++) {
    sb.append(new StringBuilder(arr[i]).reverse());
    sb.append(" ");
}

```

따라서 **각 단어마다 새로운 인스턴스를 생성**하고 해당 인스턴스에서만 역순(.reverse())를 수행하여 sb에 추가하는 것이 효과적이다. 

🎯 **이유: 각 단어마다 별도의 StringBuilder가 필요하기 때문**
StringBuilder는 mutable(변경 가능한) 클래스이기 때문에 하나의 StringBuilder 인스턴스 재사용시 아래와 같이 이전 결과 누적, 혼합등 복잡해진다. 
```java
StringBuilder sbTemp = new StringBuilder();
for (int i = 0; i < arr.length; i++) {
    sbTemp.setLength(0);  // 내용 초기화
    sb.append(sbTemp.append(arr[i]).reverse());
    sb.append(" ");
}
```
#### 2. split("")함수의 용도와 결과
split("");함수는 함수 안의 어떠한 공백의 유형을 기준으로 나누어 배열에 저장하는 역할이다. 위의 코드에서 
```java
arr = cmd.trim().split(" ");  
```
를 하게되면 cmd가 "This is Java"를 arr ={ "This", "is", "Java"}로 나누게 된다. 

>느낀점

StringBuilder의 메소드의 반환형과 사용시 인스턴스를 어떻게 선언하고 사용해야하는지 느낀 중요한 문제였다. 또한 Split()함수를 적재적소에 활용할 수 있다는 자신감을 키워준 문제였다. 
