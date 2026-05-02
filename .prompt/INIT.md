# 量子信息基础大作业

## 选题

>课题二：基于 Streamlit 的交互式布洛赫球（Bloch Sphere）与单比特门演化演示:
>
>布洛赫球是理解量子态叠加的直观工具。学生需利用 Qiskit 或 QuTiP 的可视化模块，结合 Streamlit 框架，开发一个交互式 3D 布洛赫球工具。用户可选择作用泡利门（X, Y, Z）、Hadamard 门或任意旋转门（Rx, Ry, Rz），程序需通过 3D 动画实时展示量子态矢量在球体上的旋转轨迹。

## 选题详情信息

详见`.doc/`中的文件

## 项目基本环境

1. 基于wsl2的fedora环境
2. 已安装git miniforge环境

## 基本要求

1. 使用git进行严格的项目管理
2. 使用wsl环境下的conda（miniforge）进行python环境的管理，为本项目单独创建一个环境，自行命名（字符不多于5个）。并在项目根目录下创建`env`文件夹，记录环境配置要求，并配置linux与win下的一键环境配置脚本
3. 要求项目要有详细的README文档，中英文版本各一个
4. 要求该项目在win和linux平台上均可以正常运行
5. 再额外生成一个学术化的项目报告，要求包含原理分析、结果记录等内容

## UI交互风格要求

1. 使用高度自定义的交互界面风格，不要拘泥于默认的风格和AI常用的配色风格
2. 大致风格采用复古未来主义
3. 配色采用黑橙配色，展现上世纪的科技风
4. UI上谨慎使用圆角，可以参考上世纪的硬朗直角风格，体现实用主义
5. UI排版合理，信息密度中上，增强页面体现的有效信息
6. 参考我给你安装的skills：
   - addressing-pr-review-comments ./.agents/skills/addressing-pr-review-comments
       Agents: Claude Code, GitHub Copilot, OpenCode
     assessing-external-test-risk ./.agents/skills/assessing-external-test-risk
       Agents: Claude Code, GitHub Copilot, OpenCode
     checking-changes ./.agents/skills/checking-changes
       Agents: Claude Code, GitHub Copilot, OpenCode
     creating-pull-requests ./.agents/skills/creating-pull-requests
       Agents: Claude Code, GitHub Copilot, OpenCode
     debugging-streamlit ./.agents/skills/debugging-streamlit
       Agents: Claude Code, GitHub Copilot, OpenCode
     discovering-make-commands ./.agents/skills/discovering-make-commands
       Agents: Claude Code, GitHub Copilot, OpenCode
     finalizing-pr ./.agents/skills/finalizing-pr
       Agents: Claude Code, GitHub Copilot, OpenCode
     fixing-flaky-e2e-tests ./.agents/skills/fixing-flaky-e2e-tests
       Agents: Claude Code, GitHub Copilot, OpenCode
     fixing-streamlit-ci ./.agents/skills/fixing-streamlit-ci
       Agents: Claude Code, GitHub Copilot, OpenCode
     frontend-design ./.agents/skills/frontend-design
       Agents: Claude Code, GitHub Copilot, OpenCode
     generating-changelog ./.agents/skills/generating-changelog
       Agents: Claude Code, GitHub Copilot, OpenCode
     implementing-feature ./.agents/skills/implementing-feature
       Agents: Claude Code, GitHub Copilot, OpenCode
     improving-frontend-coverage ./.agents/skills/improving-frontend-coverage
       Agents: Claude Code, GitHub Copilot, OpenCode
     improving-python-coverage ./.agents/skills/improving-python-coverage
       Agents: Claude Code, GitHub Copilot, OpenCode
     sharing-pr-agent-artifacts ./.agents/skills/sharing-pr-agent-artifacts
       Agents: Claude Code, GitHub Copilot, OpenCode
     understanding-streamlit-architecture ./.agents/skills/understanding-streamlit-architecture
       Agents: Claude Code, GitHub Copilot, OpenCode
     updating-internal-docs ./.agents/skills/updating-internal-docs
       Agents: Claude Code, GitHub Copilot, OpenCode
     writing-spec ./.agents/skills/writing-spec
       Agents: Claude Code, GitHub Copilot, OpenCode