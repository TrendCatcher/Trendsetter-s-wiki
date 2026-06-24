---
title: "[Java Doc] Hash Set "
date: 2024-02-19 08:08:27
url_slug: "Java-Doc-Hash-Set"
---

[reference : [youtube: 쉬운코드](https://www.youtube.com/watch?v=IkImFugfFQk&t=204s)]
# Set 자료형 소개
Set은 데이터를 저정하는 추상 자료형이자 순서를 보장하지 않는 자료형이다. 
**(NO guarantees as to the iteration order of the set)**
중복 또한 허용하지 않고, 데이터 조회가 List보다 빠르다는 장점이 있다. 

# Set 관련 동작들 (All Methods)
![](https://velog.velcdn.com/images/trendsetter/post/d547b90e-0a6e-42d7-b53e-9156e70356c1/image.png)
처음보시는 분들은 조금 현기증이 날 수 도 있겠지만 필자는 javaDoc을 보는 습관을 들이기 위해 다음과 같이 소개한다. 먼저, **주요 동작**들을 먼저 살펴본다. 
1. `add(E e)`
-  직역하면, 지정한 요소가 아직 없는 경우 set에 추가하는 동작(메소드)이다. 쉽게 말해,add(10), add(20), add(30)을 하면 set에 10,20,30이 추가 된다. 단, add(10)이라는 연산을 추가할 경우 set은 중복을 제거하기 위해 사용하는 자료형 이므로 10이 추가되지 않고 아무 동작을 하지 않는다. 

```java
public boolean add(E e){
	return map.put(e,PRESENT)==null;
}
//e는 키이고 value자리에는 PRESENT라는 더미데이터를 넣는다. 
// 즉, put()메서드의 결과 값이 null이면 현재 있는 set에 해당 요소가 없다는 뜻이고 null이 아니면 요소가 set에 있다는 의미이다. 
```

2. `contains(Object o)` 
- set에 해당 원소가 있으면 `true`를 반환한다. key를 조회한다.
```java
public booelan contains(Object o){
	return map.containsKey(o);
}
//map에 key의 존재여부 확인
```
3. `remove(Object o)`
- 지정한 요소가 set에 있는 경우 제거한다. 

# set 사용하는 이유
크게는 2가지 이다. 
1. 중복을 제거하기 위해 사용

2. 데이터의 존재여부를 확인하기 위해 사용한다. 
![](https://velog.velcdn.com/images/trendsetter/post/802670a4-17c4-4cc4-aa52-57943f79c995/image.png)
- set은 데이터 존재유뮤 확인을 List보다 빨리하기 때문에 그림에서 오른쪽 경기도 지원 사업 수혜자를 set으로 관리해서 더 빨리 조회(Search)할 수 있게한다. 

# Set 구현체 
1. Hash set()
- hash table(hash function을 통해 구현됨), key를 hash function의 input으로 넣고 나온 output인 hash(integer)를 배열의 capacity(array size) 만큼 modular연산을 해서 나온 값을 index로 사용해서 적절하게 value를 배치한다. 
- [장점] 일반적으로 **테이블의 크기와 상관없이** key를 통해 상수시간에 빠르게 데이터에 접근이 가능하다. 
- 그래서 hash set은 이런 hash table을 사용해서 구현하기 때문에 **크기 상관없이** 데이터 조회가 빠른 것이다. 
- 새로운 비어있는 set을 구성한다. 백업 HashMap 인스턴스의 기본 초기 용량(16)과 로드 팩터(0.75)가 있다. 로드 팩터(load factor)란, HashMap 클래스의 구현(implementation)에 사용되는 파라미터로, 더 많은 원소를 수용하기 위해 hash table의 크기 조정을 위해 존재한다. 

- 사용 예제
```java
Set<String> unique = new HashSet<>();
unique.add("subscribe");
unique.add("good");
unique.add("subscribe");

System.out.println(unique.size());	// 2
System.out.println(unique.contains("subscribe"));	// true
System.out.println(unique.contains("alarm Settings"));	// false


```
2. linked hash set(java)
3. tree set(java)


# 느낀점
항상 자바독을 공부하면서 기본이 중요하다는 생각을 한다. 정확한 동작원리와 자료형등을 이해해야 나중에 실무에서도 hashset이나 hashmap을 활용할 때 더 정확하고 빠르게 할 수 있음을 다시 깨닫는다. 

또한 독서도 중간에 정리하면서 읽으면 시간을 아끼듯이 이번 포스팅을 통해 hashSet과 Map에 대해 정리하면서 확실히 이해하는 것에 뿌듯했다! ^^ 
꾸준함 && 열정 ❤
