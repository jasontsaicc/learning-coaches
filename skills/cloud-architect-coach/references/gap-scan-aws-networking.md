# P1 Networking Gap-Scan

## Protocol

學員自評對 AWS networking 熟悉,這一關把「熟悉」拿去測、不拿去信。coach 口頭問下面 16 題,學員不看筆記直接答。這不是上課、也不是 lab,唯一目的是定位缺口。

每題按三級評分,標籤寫進 progress file,維持英文原字:

- `pass`:答到 mechanism level。講得出「為什麼會這樣運作」,不是只點出服務名稱。
- `shaky`:點名對了,但講不出機制。知道要用哪個東西,說不清它底下怎麼動。
- `hole`:卡住,答不出來。

評分靠每題後面的 "listen for" 那行判斷:那行列的機制,學員要自己講出來才算 `pass`。

`shaky` 跟 `hole` 的每一題當場變成一堂 mini-lesson,補完機制。補完不算過關:所有 `shaky` / `hole` 的題目,都在後面的 session 重測一次,P1 才會關。retest 通過前 P1 不 close。

結果記進 progress file,欄位與格式依 `engine/PROGRESS-SCHEMA.md`,這裡不重新定義 schema。

## Questions

1. Private-subnet 的 EC2 要連到 S3,有三種做法,各在什麼情況下選?
   listen for: NAT+IGW vs gateway endpoint vs interface endpoint;三者的成本與 policy 取捨。

2. SG 跟 NACL 的差別,stateful / stateless 在封包層是什麼意思?
   listen for: connection tracking;回程流量怎麼被放行;交叉參考 `skills/k8s-coach/references/foundations-linux-network.md` §3.5 conntrack。

3. 連某個 port,拿到 Connection Refused 跟拿到 Timeout,在 VPC 裡各代表什麼?
   listen for: refused = 活著的主機沒有 listener,回你一個 RST;timeout = SG/NACL 靜默丟包。

4. TGW 跟 VPC peering,peering 在什麼時候開始不 scale?
   listen for: 沒有 transitive routing;n-squared mesh;route-table 上限。

5. Direct Connect 跟 site-to-site VPN 怎麼選,為什麼真實設計常常兩個一起上?
   listen for: latency 的一致性、頻寬、成本;VPN 當 DX 的 failover。

6. 在 DX 或 VPN 連線上,BGP 在做什麼?
   listen for: route 的廣播 / 傳播、path selection、為什麼 static route 到後面不 scale。

7. On-prem 主機要解析 Route 53 private hosted zone 裡的記錄,VPC 內的 workload 又要解析 on-prem 的名稱,怎麼做?
   listen for: Resolver inbound + outbound endpoints;forwarding rules。

8. 在 EC2 instance 裡面,`/etc/resolv.conf` 指的那個位址,是誰在回答?
   listen for: VPC+2 / 169.254.169.253;Route 53 Resolver。

9. ALB 跟 NLB:各在哪一層、TLS termination 的選項、source IP 保不保得住?
   listen for: L7 vs L4;X-Forwarded-For vs proxy protocol。

10. 走一遍 TLS handshake,以及憑證鏈怎麼被驗證。你會把 TLS 終結在哪、為什麼?
    listen for: chain of trust 一路連回 root CA;ALB termination 搭 ACM;再加密回 backend(re-encrypt)。

11. VPC route table 怎麼挑一條 route?
    listen for: longest-prefix match;local route;一個 subnet 對一張 table。

12. 客戶的 on-prem CIDR 跟 VPC CIDR 重疊,會壞什麼、有哪些選項?
    listen for: routing 變得有歧義;private NAT gateway;re-IP。

13. MTU:VPC 內 vs 走 VPN / DX,blackhole 長什麼樣?
    listen for: 9001 vs 1500;PMTUD 被 ICMP filtering 擋掉;小封包過得去、大封包卡死。

14. NAT gateway 做什麼、不做什麼,它的成本與設計陷阱在哪?
    listen for: 不接受 inbound;per-AZ 放置;data-processing 費用。

15. 兩個帳號要共用一個網路,有哪些選項、各自的取捨?
    listen for: RAM shared VPC vs TGW vs peering。

16. FSI 客戶要求所有 egress 都要被檢查、而且不能碰公網,畫出這個 egress 設計。
    listen for: 不放 IGW;透過 TGW 走 centralized egress;Network Firewall 或 proxy;SG 的 egress 規則。
