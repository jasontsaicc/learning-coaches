# North Star

## Win Condition

通過大廠 senior DevOps/SRE 面試 + 拿到外商 package。

**Derivation:**
- 「打穿底層原理」是手段,不是目的。預設做法是把每個 k8s 機制打穿到底層(OS/網路/分散式/控制理論),因為這同時服務「面試表現」與「真實變強」,兩者通常一致。
- 面試窗口與跑道的戰略層規劃在 `workspaces/k8s/curriculum-plan.md`(advisory);runtime 真相永遠在 progress.md。
- 純速度型訓練(kubectl 手速、背 YAML 欄位)降為副線;CKA 是里程碑不是目的(時點與形式見 curriculum-plan §4.8)。
- coding / DSA round 外包給家族成員 `leetcode-coach`,system design 外包給 `sd-coach`,本 coach 不重造。

## Tie-Break Rule

當「面試 ROI」與「變強深度」分歧時,**面試贏**。

**Derivation:**
- 北極星統治所有取捨:每個決定回頭問一句「這對通過大廠面試 + 拿 package 有幫助嗎?」
- 不主動破壞變強:只在資源(時間/精力)衝突時才砍深度,不是例行性犧牲。
- 底層原理可無限遷移,這是「加速度 > 速度」的本錢,所以深度通常就是最高的面試 ROI;真正需要仲裁的是枝節深潛(例如 etcd Raft 實作細節),這類 park 到對應 phase 或捨棄。
