# molecule_rotation

## nonlinear inverse problem

Повороты графа в пространстве. СЛАУ в ней нет, зато задача обратная, и включает не только локальную, но и глобальную оптимизацию.

Пусть дана информация о структуре молекулы в формате JSON из базы данных PubChem. Пример: молекула аспирина.

Программа должна распарсить JSON (только атомы с координатами и связи с кратностями, игнорируя заряды и прочую дополнительную информацию), построить в памяти граф молекулы (вершины = атомы, рёбра = связи) и определить рёбра, которые одновременно:

-  одинарные (т. е. соответствуют одинарным, а не двойным и не тройным связям)
-  не принадлежат циклам
-  не являются "висячими", т. е. продолжаются с обоих концов

В вышеупомянутой молекуле аспирина таких рёбер четыре (если смотреть на двумерную картинку, в которой не показаны водороды); в трёхмерной картинке с водородами таких рёбер можно насчитать пять.

Далее, программа должна повернуть молекулу в трёхмерном пространстве вокруг каждого из найденных рёбер на случайный угол так, чтобы вращалась не вся молекула, а лишь "половина", лежащая по одну сторону от ребра. Координаты атомов при этом, конечно, изменятся, изменится форма молекулы.

Далее, программа должна забыть случайные углы, проанализировать получившиеся координаты атомов и найти такие углы вращения вокруг найденных связей, чтобы атомы встали на исходные места. Один из способов это сделать: сгенерировать множество случайных наборов углов и из каждого из них градиентным или покоординатным спуском приблизить атомы к исходным положениям.
