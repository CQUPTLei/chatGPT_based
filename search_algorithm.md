# 一、广度优先搜索算法

**广度优先搜索**（Breadth-First Search，BFS）是一种图形搜索算法，用于在图形中搜索最短路径。在广度优先搜索中，按照距离起点逐渐增加的顺序搜索图形。也就是说，先搜索距离起点最近的所有节点，再搜索距离较远的节点。

广度优先搜索使用一个队列来存储待搜索的 节点。首先将起点节点放入队列中，然后重复以下过程，直到队列为空：

1. 取出队列中的第一个节点。

2. 将该节点的所有相邻节点加入队列。
3. 标记该节点已被搜索过。

在广度优先搜索中，由于我们优先搜索距离起点较近的节点，因此如果存在多条可到达目标节点的路径，广度优先搜索将找到最短的路径。

下面是广度优先搜索的伪代码：

```
function BFS(graph, startNode, targetNode):
  // 创建队列，并将起点节点加入队列
  queue = [startNode]
  // 创建一个记录节点是否被搜索过的数组
  visited = []
  // 重复以下过程，直到队列为空
  whil equeue is not empty:
  // 取出队列中的第一个节点
	currentNode = queue.pop(0)
	// 如果该节点为目标节点，则结束搜索
	if currentNode == targetNode:
	return
	// 将该节点的所有相邻节点加入队列
	for neighbor in graph[currentNode]:
if neighbor not in visited:
queue.append(neighbor)
// 标记该节点已被搜索过
visited.append(currentNode)

// 如果没有找到目标节点，则返回null
return null
```

广度优先搜索的时间复杂度为O(V + E)，其中V是图中节点的数量，E是图中边的数量。广度优先搜索通常使用在寻找最短路径、求最小生成树等问题中。



<hr>

# 二、深度优先搜索算法

**深度优先搜索**（Depth-First Search，DFS）是一种图形搜索算法，用于搜索图形中的路径。在深度优先搜索中，我们沿着边走到尽可能深的地方，然后再回溯到起点或其他可行路径，直到找到目标节点为止。

深度优先搜索使用一个栈来存储待搜索的节点。首先将起点节点放入栈中，然后重复以下过程，直到栈为空：

1. 取出栈中的最后一个节点。
2. 将该节点的所有相邻节点加入栈。
3. 标记该节点已被搜索过。

下面是深度优先搜索的伪代码：

```
function DFS(graph, startNode, targetNode):
  // 创建栈，并将起点节点加入栈
  stack = [startNode]
  // 创建一个记录节点是否被搜索过的数组
  visited = []
  // 重复以下过程，直到栈为空
  while stack is not empty:
    // 取出栈中的最后一个节点
    currentNode = stack.pop()
    // 如果该节点为目标节点，则结束搜索
    if currentNode == targetNode:
      return
    // 将该节点的所有相邻节点加入栈
    for neighbor in graph[currentNode]:
      if neighbor not in visited:
        stack.append(neighbor)
    // 标记该节点已被搜索过
    visited.append(currentNode)

// 如果没有找到目标节点，则返回null
return null
```

深度优先搜索的时间复杂度为O(V + E)，其中V是图中节点的数量，E是图中边的数量。深度优先搜索通常用于寻找图形中的环、检测图形的连通性、求解最小生成树等问题。
