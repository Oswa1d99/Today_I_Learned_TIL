## 백트래킹

백트래킹(Backtracking)은 해를 찾는 도중, 현재 경로가 더 이상 유망하지 않다고 판단되면 이전으로 되돌아가 다른 경로를 탐색하는 문제 해결 전략이다.  
트리로 주어지거나, 트리 형태로 간주할 수 있는(eg. 2차원 배열) 모든 상황에 적용 가능하다.  

흔히 DFS(깊이 우선 탐색)와 비교되는데, 백트래킹은 가지치기(Pruning)가 적용된 DFS라고 생각하면 이해하기 수월하다.  
DFS가 모든 경로를 끝까지 탐색하는 완전 탐색 알고리즘이라면, 백트래킹은 '유망성 검사(Promising Check)'를 통해 불필요한 경로를 조기에 차단한다.  

<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/a8f302ea-6e22-4c30-84b7-6253327ffde0" />

n-Queens, 부분집합의 합, 0-1 배낭문제 등의 많은 문제에서 완전 탐색을 사용한다면 시간 초과 판정을 받기 십상이다.  

따라서 모든 리프 노드까지 탐색할 필요 없이, 특정 경로가 해가 될 가능성이 없다고 판단되면(Not Promising), 그 하위 트리 전체를 탐색 대상에서 제외하고 이전 선택 지점으로 되돌아가는(Backtrack) 전략을 차용하는 것이 '해결' 판정을 받는 데 필수적이다.

이처럼 백트래킹은 DFS를 기반으로 해 구현의 기본 구조는 단순하지만, 문제의 제약 조건을 정확히 반영하여 '가지치기' 기능을 수행하는 **유망성 검사(Promising) 함수의 논리를 설계**하는 것이 핵심이자 가장 까다로운 부분이다.  

백트래킹을 대표하는 문제 몇몇을 풀어보면서, 그 개념을 익혀보자.

---

### N-Queens (백준 9663)
N X N 사이즈의 체스판에서 행/열/대각선 방향으로 체스판 끝까지 이동이 가능한 퀸 N개를 동선 상 겹치지 않게 두는 문제이다.  

이 문제를 해결하는 가장 단순한 논리적 흐름은 다음과 같다:  
> 퀸을 하나씩 두면서, 이전 퀸의 행/열/대각선 방향과 겹치지 않는지 확인한다

이 문제를 가장 단순하게 접근하면, N X N개의 칸 중 퀸을 놓을 N개의 칸을 선택하는 모든 조합을 확인하는 것이다.
4-Queens의 경우 16개의 칸 중 4개를 선택하는 것이므로, 총 16C4 = 1,820가지의 경우를 모두 확인해야 한다.  

하지만 여기서 문제의 제약 조건을 활용한 '작은 트릭'이 유용하게 쓰인다.  
바로 **어차피 각 행에는 퀸이 반드시 하나만 존재한다**는 사실을 이용해, 탐색의 구조 자체를 바꾸는 것이다. 
즉, "어떤 칸에 놓을까?"가 아니라 "1번 행에는 몇 열에 놓을까?", "2번 행에는 몇 열에 놓을까?" 로 문제를 재정의한다.  

(만약 2차원 그래프를 그대로 풀이에 사용한다면, 테스트 케이스(n=8)일 때는 통과하지만 n이 더욱 커질 때는, 그래프의 크기로 인해 시간복잡도에 추가된 N으로 인해 시간 초과 판정을 받는다)

이렇게 하면 각 행마다 N개의 열 중 하나를 선택하는 문제가 되므로, 탐색 공간의 크기가 대략 N^N수준으로 줄어듭니다. 
4-Queens의 경우 4^4 = 256가지로, 1,820가지에 비해 경우의 수가 크게 감소한다.  
백트래킹은 이 256가지의 가능성 속에서 유망하지 않은 경로를 더 쳐내는 역할을 수행할 것이다.  

지금까지의 전제를 바탕으로, Promising 함수를 설계해보자.  
같은 행 조건은 이미 전제로 두었으니 Promising 함수에서는 고려하지 않는다.  
이 함수에서 확인해야 할 것은 "이전 퀸과 하나라도 같은 열에 존재하는지"와 "이전 퀸과 대각선 방향에서 겹치는지"다.  
열에 관한 부분은 어렵지 않게 떠올릴 수 있지만, 대각선 방향은 그림을 그려서 생각해보는 편이 유리하다.  

<img width="442" height="424" alt="image" src="https://github.com/user-attachments/assets/4bb90f97-efd5-4200-9c0b-fb650940be76" />

좌측 상단 모서리를 (0, 0)으로, 우측 하단 모서리를 (3, 3)으로 하는 체스판을 가정하겠다.   
이 때 대각선 조건이 되는 상황을 몇 개 적어보면 다음과 같은 규칙을 발견할 수 있다.
> 두 퀸 사이의 X 좌표의 차와 Y 좌표의 차가 같다면, 두 퀸은 대각선 방향에 놓인다.

특정 노드의 가능성을 검사하는 Promising 함수는 부모 노드들을 하나씩 검사하면서, 
조건에 위배된다면 바로 False를 반환하고 모두 동선이 겹치지 않았을 때만 True를 반환하도록 구현하면 된다.

예를 들어, 기존 (0, 0)과 (1, 3) 위치에 퀸이 놓인 체스판에서 추가로 (2, 2) 위치에 퀸을 놓는다면  
(0, 0)과의 조건을 검사할 때는 무사히 통과하지만 (1, 3)과의 검사에서는 '대각선' 조건에 위배되어 False를 반환할 것이다.

```
import sys

n = int(sys.stdin.readline().strip())
count = 0

graph = [0] * (n) # 일차원 배열 eg. [0, 3, 1, 2] -> (0,0), (1,3), (2,1), (3,2)에 퀸 존재
def promising(row, col):
    for prev_row in range(row): # 이전 행을 검사
        prev_col = graph[prev_row] # 이전 행에서 어떤 열에 퀸을 놓았는지
        if prev_col == col or (row - prev_row) == abs(col - prev_col): 
            # 이전 퀸과 같은 열에 놓였거나, 대각선에 위치했다면
            return False
    return True
```

이제는 재귀적으로 트리를 깊이 우선으로 탐색하면서, Promising 함수의 반환값에 따라 가지 치기 여부를 결정한다.  

```
def solution(row):
    global count
    
    if row == n:
        count += 1
        return
    
    for col in range(n):
        if promising(row, col):
            graph[row] = col
            solution(row + 1)
            graph[row] = 0
       
                
solution(0)
print(count)
```

백트래킹의 시간 복잡도는 최악의 상황에서 (N-Queens 함수의 호출 횟수) * (각 호출에서 노드 방문 횟수) = O(N) * O(N!) = O(N!) 이지만, 
가지치기를 이용한 덕분에 실제 작동 시간은 이보다 적다.

---
### 스도쿠 (백준 2580)

이 문제를 푸는 방법은 Promising 함수를 어떻게 설계하느냐에 따라 두 가지로 나뉜다.
1. Promising 함수 호출 시마다 그래프를 순회하면서, 가능성 있는 해답인지 탐색
2. 가능성 여부를 미리 배열에 저장해둬, Promising 함수에서는 그 배열을 탐색

쉽게 말하자면, 1번과 2번은 **시간-공간 트레이드오프**를 잘 보여주는 예라고 할 수 있다.  

1번에서의 Promising은 메모리 공간을 아껴 대략 O(9)만큼의 시간 복잡도를 차지하고, 2번에서의 Promising은 메모리 공간을 더 쓰는 대신 O(1) 만큼의 시간 복잡도를 차지한다.  

일반적으로 코딩 테스트에서는 시간 복잡도를 최적화하는 것이 우선 과제이므로 2번이 더 바람직한 접근법이라고 말할 수 있다.  
일단, 직관적인 풀이에 가까운 1번 방법론으로 풀이한 이후에 2번 방법론으로 전환해보도록 하겠다.  

#### 1번

스도쿠 문제는 단순화하면 해당 위치의 값이 0인 인덱스에 대해서 적절한 값으로 바꿔주는 문제이다.  
이를 해결하기 위해서는, 배열의 값을 입력받을 때, 값이 0인 인덱스를 저장해두는 것이 편리하다.

```
import sys

graph = [] # 스도쿠 판
zeros = [] # 값이 0인 인덱스 튜플의 리스트

for i in range(9):
    data = list(map(int, sys.stdin.readline().split()))
    graph.append(data)

    for j in range(9):
        if graph[i][j] == 0:
            zeros.append((i,j))
```

이제 promising 함수를 설계해보자.  
1번 접근법은 (row, col)에 특정 숫자를 넣었을 때, 스도쿠의 조건을 만족하는지를 일일히 검사하는 것이다.

3x3 사각형에서 조건을 검사하는 방법은 익숙하게 느껴지지 않으므로, 숙지해두도록 하자.
- (row, col) 위치의 값이 몇 번째 사각형에 속하는가?
    - (row // 3), (col // 3) 번째 사각형     

```
def promising(row, col, num):
    for i in range(9):
        # 이미 해당 row에 원하는 숫자가 존재한다면
        if graph[row][i] == num:
            return False
    for i in range(9):
        # 이미 해당 col에 원하는 숫자가 존재한다면
        if graph[i][col] == num:
            return False

    start_row = (row // 3) * 3 # 각 사각형마다 세로 길이가 3
    start_col = (col // 3) * 3

    # (?, ?) 번째 사각형의 시작점에서 행렬로 3칸씩 검사
    for i in range(3): 
        for j in range(3):
            if graph[start_row + i][start_col + i] == num:
                return False
    return True # 행 / 열 / 사각형 조건을 모두 통과하면
```

이제 값이 0인 위치들에 대해서, promising 함수를 대입시켜 어떤 숫자로 바꿔주는 것이 적절한지 구현해주면 된다.  

이때, base condition에 도달하면 return이 아니라, 변경된 그래프 값을 출력하고 프로그램을 완전히 종료(exit)해야 한다.  

```
def solve(index):
    if index == len(zeros):
        for i in range(9):
            print(' '.join(map(str, graph[i])))
        exit() # 프로그램 완전히 종료

    row, col = zeros[index]
    for num in range(1, 10): # 어떤 숫자를 넣어야 가능한지 순회를 돌면서 검사
        if promising(row, col, num):
            graph[row][col] = num
            solve(index + 1)
            # 백트래킹 (여기까지 실행이 됐다는 것은 가망성이 없는 num이라는 것)
            graph[row][col] = 0

solve(0)
```

위의 방식대로 구현하면 실행까지 대략 2000ms 정도 걸린다.  
경우에 따라 시간 초과 판정을 받거나, 아슬아슬하게 통과하는 정도일 뿐이다.  

이제 이 방식에서 row_check, col_check, square_check라는 세 Boolean 배열을 도입하여 최적화해보자.  

#### 방법 2

사용자에 입력에 따라 graph를 채우고, zeros 배열에 0인 값의 위치를 기록하는 절차까지는 동일하다.  

다만, 그 직후에 graph를 순회하면서 Boolean 배열을 기록해준다.  

```
# n번째 row와 col에 1부터 10까지의 숫자가 사용됐는지 상황을 기록
row_check = [[False] * 10 for _ in range(9)]
col_check = [[False] * 10 for _ in range(9)]
# 각 3x3 사각형에 1부터 10까지 숫자가 사용됐는지 기록
square_check = [[False] * 10 for _ in range(9)] # 3x3 사각형이 총 9개 존재

for i in range(9):
    for j in range(9):
        num = graph[i][j]
        if num != 0:
            row_check[i][num] = True
            col_check[j][num] = True

            square_row = (i // 3) # 세로 방향으로 몇 번째 사각형인지
            square_col = (j // 3)
            square_num = 3 * square_row + square_col # (row, col)을 flatten

            square_check[square_num][num] = True
       
```
이 방식을 통해서 이후에 promising 함수에서는, 매번 graph를 순회하는 것이 아니라 Boolean 배열에 인덱스로 접근하기만 한다.

```
def promising(row, col, num):
    # 각 row와 col, (row, col)이 속한 사각형에 대해서 num이 들어가도 문제가 없을 때
    square_idx = (row // 3) * 3 + (col // 3)
    if not row_check[row][num] and \
    not col_check[col][num] and \
    not square_check[square_idx][num]:
        return True

    return False
```

이제 방법 1과 똑같이 solve 함수를 구현하면 된다.
단, 이전과 달리 해당 선택지를 골랐을 때와 백트래킹 했을 때, Boolean 배열의 값을 관리해야 한다.

```
def solve(index):
    if index == len(zeros):
        for i in range(9):
            print(' '.join(map(str, graph[i])))
        exit()
    
    row, col = zeros[index]
    for num in range(1, 10):
        if promising(row, col, num):
            graph[row][col] = num
            row_check[row][num] = True
            col_check[col][num] = True
            square_check[3*(row // 3) + (col // 3)][num] = True
    
            solve(index + 1)

            graph[row][col] = 0
            row_check[row][num] = False
            col_check[col][num] = False
            square_check[3*(row // 3) + (col // 3)][num] = False
        
solve(0)
```

방법 2 코드의 실행 시간은 대략 700ms로, 방법 1에 비해 3배 정도 줄어들었다.  
물론 메모리 공간은 기존에 비해 3배가 늘어났지만, 공간 복잡도의 빅오 표현은 O(N^2)으로 동일하다.  



---
Reference:  
https://youtu.be/z4wKvYdd6wM  
https://www.geeksforgeeks.org/dsa/4-queens-problem/
