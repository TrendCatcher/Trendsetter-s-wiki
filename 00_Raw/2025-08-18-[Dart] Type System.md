---
title: "[Dart] Type System "
date: 2025-08-18 10:31:18
url_slug: "Dart-Type-System"
---

Dart는 Type Safe을 핵심으로 하며, 이는 **사운드 타이핑**이라고도 불린다. 사운드 타입 시스템은 컴파일 시점의 **정적 타입 검사**(static type checking)와 **런타임 검사**을 결합하여, 변수의 값이 항상 변수의 정적타입과 일치하도록 보장한다. 

>[다트 공식문서 ](https://dart.dev/language/type-system)

![](https://velog.velcdn.com/images/trendsetter/post/43edb02f-2991-4de5-b833-70fe200a7d0a/image.png)

타입지정은 의무적이지만 타입 어노테이션은 선택사항이다. 이유는 type inference라고 했다. 그럼 type inference란 뭘까?

### 핵심요약

#### 타입 안전성 및 사운드 타이핑
다트 언어는 정적 및 런타임 검사를 통해 변수 값이 항상 정적 타입과 일치함을 보장하는 사운드 타입을 지닌다. 

#### 타입 어노테이션의 선택성
타입은 필수 적이지만, 타입 추론 덕분에 타입 어노테이션은 선택사항이다. 

#### 사운드 타입 시스템의 이점
버그 조기 발견, 코드 가독성 및 유지보수성 향상, AOT(Ahead-of-Time) 컴파일 효율성 증대

#### 정적 분석 팁

#### 런타임 검사

#### type inference (타입 추론)
`analyzer`는 필드, 메소드, 지역변수와 대부분의 제너릭 타입 매개변수를 위한 **1. type을 추론**한다. 만약 `analyzer`가 특정 타입을 위한 정보가 충분하지 않다면 **2. `dynamic` type**을 사용한다. 

다음은 제너릭에 적용되는 예시이다. `arguments`라는 이름의 변수는 키-값 쌍으로 된 다양한 타입의 값을 가지는 맵을 가지고 있다. 
만약 타입을 명시적으로 저장한다면 다음과 같을 것이다. 
```dart
Map<String,Object> arguments =  {'argA': 'hello', 'argB': 42};
```

대안으로, var와 final을 사용하고 Dart로 부터 추론하게 할 수 있다. 
```dart
var arguments = {'argA': 'hello', 'argB': 42};
```

map 리터럴은 그것의 엔트리들로부터 자신의 타입을 추청하고나서 맵 리터럴 타입으로부터 변수가 타입을 추론한다. 이 맵에서는 키는 모두 string이지만 값은 다른 타입을 지니고 있다. 따라서 맵 리터럴은 `Map<String, Object>`타입을 가지고 있고 `arguments` 변수도 그러하다. 

#### 필드와 메서드 추론
특정 타입이 없고 부모 클래스로부터 필드나 메소드를 오버라이드하는 필드나 부모클래스의 메서드나 필드의 타입을 메서드는 상속받는다.

초기 값을 선언했지만 선언하거나 상속 타입이 없는 필드는 그 초기 값에 기반하여 추론 타입을 가지게 된다. 

#### static 필드 추론
static필드와 변수는 그들의 initializer로부터 타입을 추론받는다. 무한 반복문이 걸리면 타입추론은 실패한다는 사실을 기억하라. 
(that is, inferring a type for the variable depends on knowing the type of that variable).
변수를 위한 타입 추론은 그 변수의 타입을 아냐 모르느냐에 달려있다는 뜻이다. 

#### 지역변수 추론
지역변수 또한 intializer로 부터 타입추론을 받는다. 
Subsequent assignments are not taken into account. 
이후의 할당은 고려되지 않는다(?)
즉, 
Dart가 변수의 타입을 결정할 때 **초기값(initializer)**만 보고 판단하며, 나중에 그 변수에 어떤 값이 할당될지는 고려하지 않는다는 의미다. 

#### 타입 매개변수 추론 
생성자 호출이나 제네릭 메서드 호출 시 arguments(매개변수)는 호출이 발생하는 문맥(context)으로부터의 아래 방향(downward) 정보와 생성자 또는 제네릭 메서드의 인자로부터의 위 방향(upward) 정보를 조합하여 추론됩니다. 만약 추론 결과가 의도와 다르다면, **항상 명시적으로 타입 인자를 지정**해 줄 수 있습니다

>참고 dart에서의 제너릭

```dart
T first<T>(List<T> ts){
//Do some initial work or error checking, then...
T tmp = ts[0];
//Do some additional checking or processing...
return tmp;
}
```
위의 `first`(`<T>`)의 제너릭 타입 파라미터는 다음과 같은 구체적인 위치에 매개변수 `T`를 사용하도록 허용한다.: 
- 함수의 반환타입 (`T`)
- 매개변수의 타입안에서(`List<T>`)
- 지역변수의 타입 안에서 (`T tmp`)

```dart
//Inferred as if you write <int>[].
List<int> listOfInt = [];
// Inferred as if you wrote <double>[3.0].
var ListOdDouble = [3.0];

//Inferred as Iterable<int>.
var ints = listOfDouble.map((x) => x.toInt());
```
> 참고 

x.toInt()는 double 타입인 x를 int 타입으로 변환하는 메서드

위의 예시에서 `x`는 위에서 아래로의 문맥상 `double`로 추론된다. 메서드의 클로저`((x) => ...)`의 반환타입은 아래에서 위로의 문맥 추론 정보를 사용하여 `int`로서 추론된다. 

<details>
<summary>[추가설명] 매개변수 타입 추론 </summary>

var listOfDouble = [3.0];
var ints = listOfDouble.map((x) => x.toInt());
위 코드에서 x의 타입과 map() 메서드의 타입 인자가 어떻게 추론되는지 단계별로 살펴보겠습니다.

1단계: x의 타입 추론 (아래 방향, Downward)
map() 메서드는 Iterable에 있는 각 요소에 대해 함수를 적용합니다. 이때 listOfDouble은 double 타입의 리스트이므로, Dart는 map() 메서드의 클로저((x) => ...)에 전달되는 변수 x가 double 타입일 것이라고 추론합니다. 이는 listOfDouble이라는 문맥에서부터 x로 타입 정보가 아래로(downward) 흐르기 때문입니다.

2단계: 클로저 반환 타입 추론 (위 방향, Upward)
클로저의 본문은 x.toInt()입니다. double 타입인 x에 .toInt() 메서드를 호출하면 결과는 int 타입이 됩니다. Dart는 이 결과를 보고 클로저의 반환 타입이 int라고 추론합니다. 이는 x.toInt()라는 코드에서부터 클로저의 반환 타입으로 타입 정보가 위로(upward) 흐르기 때문입니다.

3단계: map() 메서드 타입 인자 추론 (위 방향, Upward)
마지막으로, Dart는 2단계에서 추론된 클로저의 반환 타입(int)을 map() 메서드의 타입 인자(map<int>)를 결정하는 데 사용합니다. map() 메서드는 새로운 Iterable을 생성하는데, 그 요소의 타입은 클로저의 반환 타입과 동일해야 하기 때문이죠. 이 역시 클로저의 반환 타입에서 map() 메서드의 타입 인자로 정보가 위로(upward) 흐르는 과정입니다.

결론적으로, x의 타입은 아래 방향(downward) 추론을 통해 double이 되고, map() 메서드의 타입 인자는 위 방향(upward) 추론을 통해 int가 되는 것입니다. 이 두 가지 추론 방식이 결합되어 Dart는 별도의 타입 명시 없이도 정확한 타입을 결정합니다.
  </details>

  ====https://dart.dev/language/type-system#inference-using-bounds=====부터 블로깅 시작
  
다시 본론으로 돌아와, 정적 타입 체킹의 장점은 dart의 정적 analyzer를 사용하여 컴파일 시간에 버그를 찾는 능력이 장점이다. 
  
대부분의 정적 분석 에러를 제너릭 클래스들에 대한 타입 어노테이션을 추가함으로써 고칠수 있게 된다. 
대부분의 공통적인 generic 클래스들은 collection 타입인 `List<T>` 와 `Map<K,V>`이다.

예를 들어, 다음 코드의 printInts()함수는 integer list를 출력하고, main()함수는list를 생성하고 printInts()함수에 그 list를 통과시킨다. 
```dart
void printInts(List<int> a) => print(a);

void main(){
	final list =[];
  	list.add(1);
 	list.add('2'); 
  	printInts(list);
}
``` 
  
다음 코드는 `printInts(list)`의 호출에 있는 `list`에 대한 타입 에러의 결과가 난다. 
  
  ```cmd
  error - The argument type 'List<dynamic>' can't be assigned to the parameter type 'List<int>'. - argument_type_not_assignable
  ```
에러는 `List<dynamic>` 에서 `List<int>`로의 unsound 명시적 캐스트를 강조한다. `list`변수는 정적 타입인 `List<dynamic>`을 가지고 있다. 이는 `var list = []`초기화가 analyzer에게 타입 추론을 위한 dynamic보다 더 구체적인 매개변수에 대한 충분한 정보를 주지 못하기 때문에 발생한다. 
  
  
<details>
<summary>[필독!!]위코드의 상세한 설명</summary>
final list = [];: 이 코드는 list 라는 변수를 선언합니다. 하지만 Dart 컴파일러는 이 리스트에 어떤 타입의 요소가 들어갈지 알 수 없습니다. 따라서 final list = []는 List의 가장 일반적인 형태인 List<dynamic>으로 타입이 추론됩니다. dynamic 타입은 어떤 값이든 담을 수 있지만, 그만큼 타입 안전성이 떨어집니다.

list.add(1);: List<dynamic> 타입이므로 정수 1을 추가하는 것은 아무 문제가 없습니다.

list.add('2');: List<dynamic> 타입이므로 문자열 '2'를 추가하는 것도 역시 문제가 없습니다. 이 시점에서 list에는 int와 String이 섞여 있습니다.

printInts(list);: 이제 list 변수를 printInts() 함수에 전달합니다. 그런데 printInts() 함수는 매개변수로 **List<int>**만 받도록 정의되어 있습니다.
  </details>
  
   
  
