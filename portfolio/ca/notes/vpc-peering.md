# VPC Peering：用封包來回檢查連線

## 直接連線與路由

Peering 連接兩個 VPC。建立並接受連線後，來源及目的 subnet 使用的 route table 仍需有適當的去程與回程路由，target 指向該 peering connection。安全群組與 NACL 也必須允許所需流量；active 狀態本身不代表應用可達。

## 非傳遞性

A–B 與 B–C 的 peering 不會自動形成 A–C 通道。A 與 C 若要直接透過 peering 通訊，需要另外建立 A–C 連線並設定路由。不能把 B 當成 peering 中繼站。

## 位址與規模

重疊的 IPv4 CIDR 不能建立對應的 VPC peering。所有 VPC 彼此直接相連時，每條連線連接一對 VPC，所以 n 個 VPC 的完整 mesh 有 n(n−1)/2 條連線。這是拓撲計算，不代表服務配額允許任意規模。

任一 IPv4 CIDR 重疊都會阻止建立 peering，包含次要 CIDR；即使只打算使用其他不重疊的範圍也不例外。例如 A 有 `172.16.0.0/16`，B 的次要 CIDR 是 `172.16.1.0/24`，兩者仍重疊。

## 檢查順序

先確認需求與不重疊位址，再建立並接受 peering，補齊 subnet 路由表的雙向路由與安全規則，最後用實際流量驗證。排查時分清控制面狀態、路由及流量允許條件。

AWS 允許在 peering 還是 `pending-acceptance` 時先新增路由，但此時路由狀態是 `blackhole`，直到連線 `active` 才能生效。「設定已儲存」不等於「路徑可轉送」；上面的先接受再加路由是工作清單的順序，不是 API 的硬性限制。

## 官方依據

- [Peering 運作與限制](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html)
- [Peering 路由設定](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-routing.html)

2026-10-11 校對。本頁為概念練習，不建立任何雲端資源。
