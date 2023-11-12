1. 运算逻辑和进程间通信逻辑隔离/使用共享内存代替进程间通信

2. UI OCR

3. 显示库更换

4. script逻辑

5. situation 移动到 OPA模块统一更新和处理

6. 继续检查全流程性能问题

7. 使用 threading.Condition 或者 threading.Event 来代替忙等待

8. config env 分离, parameters

9. 子模块导入整个config/env, 内部对所需信息分级进行处理

10. script, OPA, situationUpdate逻辑合并

11. adb binary into vendor path