from ortools.sat.python import cp_model
import pandas as pd

def main():
    # 创建模型
    model = cp_model.CpModel()

    # 定义变量
    # x[i,j] 表示在第i块地种植第j种作物的面积
    # i: 地块编号 (1-6)
    # j: 作物编号 (1-4: 小麦、玉米、水果、蔬菜)
    x = {}
    for i in range(1, 7):
        for j in range(1, 5):
            x[i,j] = model.NewIntVar(0, 100, f'地块{i}_作物{j}')  # 上限设为100，足够大

    # 收益矩阵
    revenue = {
        (1,1): 500, (1,2): 800, (1,3): 1000, (1,4): 1200,  # 地块1
        (2,1): 550, (2,2): 700, (2,3): 960, (2,4): 1040,   # 地块2
        (3,1): 630, (3,2): 600, (3,3): 840, (3,4): 980,    # 地块3
        (4,1): 1000, (4,2): 950, (4,3): 650, (4,4): 860,   # 地块4
        (5,1): 800, (5,2): 900, (5,3): 600, (5,4): 880,    # 地块5
        (6,1): 700, (6,2): 930, (6,3): 700, (6,4): 780     # 地块6
    }

    # 目标函数：最大化总收益
    objective_terms = []
    for i in range(1, 7):
        for j in range(1, 5):
            objective_terms.append(x[i,j] * revenue[i,j])
    model.Maximize(sum(objective_terms))

    # 约束条件1：每块地的总面积不超过其面积上限
    land_limits = {1: 42, 2: 56, 3: 44, 4: 39, 5: 60, 6: 59}
    for i in range(1, 7):
        model.Add(sum(x[i,j] for j in range(1,5)) <= land_limits[i])

    # 约束条件2：每种作物的总种植面积必须满足计划面积
    crop_requirements = {1: 76, 2: 88, 3: 96, 4: 40}  # 小麦、玉米、水果、蔬菜
    for j in range(1, 5):
        model.Add(sum(x[i,j] for i in range(1,7)) == crop_requirements[j])

    # 求解问题
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 打印结果
    print("优化状态:", solver.StatusName(status))
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("\n最优种植方案:")
        print("\n地块\t作物\t面积(亩)\t收益(元/亩)\t总收益(元)")

        # 创建结果列表
        results = []
        for i in range(1, 7):
            for j in range(1, 5):
                area = solver.Value(x[i,j])
                if area > 0:  # 只打印有种植的面积
                    crop_names = {1: "小麦", 2: "玉米", 3: "水果", 4: "蔬菜"}
                    results.append({
                        "地块": f"地块{i}",
                        "作物": crop_names[j],
                        "面积": round(area, 2),
                        "单产收益": revenue[i,j],
                        "总收益": round(area * revenue[i,j], 2)
                    })

        # 转换为DataFrame并打印
        df_results = pd.DataFrame(results)
        print("\n", df_results.to_string(index=False))

        # 打印总收益
        total_revenue = sum(row["总收益"] for row in results)
        print(f"\n总收益: {total_revenue:,.2f} 元")
    else:
        print("未找到可行解")

if __name__ == '__main__':
    main() 