"""
Generate official_notes entries for 民國106年第2次醫學(三).
Writes 80 notes into docs/official_notes.json.
"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTES_FILE = "C:/Users/fred9/Desktop/Claude Code/醫師二階國考考古題/docs/official_notes.json"

NOTES = {
1: """正確答案：B

【疾病重點】酸鹼失衡判讀 — 代謝性鹼中毒（Metabolic Alkalosis）
- pH 7.51（鹼血症）、PaCO2 49 mmHg（偏高）、HCO3⁻ 38 mmol/L（明顯偏高）
- 判讀步驟：① pH 7.51 → 鹼血症 ② 看HCO3⁻ 38（升高）→ 代謝性鹼中毒為原發 ③ PaCO2 49（升高）→ 呼吸代償（低換氣）
- 代謝性鹼中毒的呼吸代償公式：預期PaCO2 = 40 + 0.7×(HCO3⁻ - 24) = 40 + 0.7×14 ≈ 49.8 → 符合
- 常見原因：嘔吐（失HCl）、利尿劑（失K⁺、H⁺）、原發性醛固酮症

【解題關鍵】pH升高（鹼血症）+ HCO3⁻升高 → 代謝性鹼中毒（選項B）。PaCO2同步升高為呼吸代償反應。""",

2: """正確答案：B

【疾病重點】失智症（Dementia）
- 最常見失智症：阿茲海默症（Alzheimer's disease，約60-70%），血管性失智症約10-20%→ A錯誤
- 血管性失智症：多次中風或腦白質病變（white matter disease）造成→ B正確
- 早期失智症：記憶力下降為最常見，但並非「一定」會有→ C錯誤
- 行為症狀治療：行為治療（非藥物）為首選，非精神藥物→ D錯誤

【解題關鍵】血管性失智症的病因為腦血管疾病（多次中風或腦白質損傷），選項B正確。""",

3: """正確答案：C

【疾病重點】高血壓急症vs.緊急症（Hypertensive Urgency vs. Emergency）
- 此患者：收縮壓190-200 mmHg，但無任何不適症狀 → 高血壓緊急症（urgency），非急症
- 舌下短效nifedipine（dihydropyridine CCB）：造成血壓急速下降 → 腦、心、腎缺血風險高 → 禁用
- 高血壓緊急症處置：休息後重測、口服降壓藥緩慢降壓（24-48小時），不可快速降壓
- 正確處置：休息再量（A）、詢問病史（B）、注意神經症狀（D）均正確

【解題關鍵】題目詢問何者「欠佳」。舌下短效nifedipine因造成血壓急速不可控下降，目前已不建議用於高血壓緊急症（選項C）。""",

4: """正確答案：C

【疾病重點】射出分率保留型心衰竭（HFpEF, Heart Failure with Preserved EF）
- EF 55%（正常）+ S3 + 舒張功能不良 + 雙肺囉音 → HFpEF（舒張性心衰竭）
- BNP/NT-proBNP：可作為心衰竭嚴重度指標 → A正確
- 限鹽：心衰竭基本飲食衛教 → B正確
- ACEi在HFpEF：目前尚無大型RCT證實可改善HFpEF的長期預後（不同於HFrEF）→ C錯誤
- 利尿劑改善症狀：HFpEF的症狀治療核心 → D正確

【解題關鍵】題目詢問何者「錯誤」。ACEi已被證明對HFrEF（低EF）有益，但對HFpEF的長期預後改善尚未確立→選項C。""",

5: """正確答案：D

【疾病重點】下壁心肌梗塞（Inferior STEMI）合併右心室梗塞
- 下壁STEMI：ST上升於II、III、aVF → A相關
- 右心室梗塞（RVMI）：V4R ST上升 → C相關（頸靜脈鼓張+低血壓為特徵）
- 下壁STEMI的鏡像變化：ST壓低於V1、V2（reciprocal changes）→ B相關
- PR段壓低（PR depression）：心包膜炎（pericarditis）的特徵，與STEMI無關 → D最不相關

【解題關鍵】題目詢問「最不可能」與下壁STEMI相關的ECG變化。PR segment depression是心包膜炎的特徵，不是STEMI的表現（選項D）。""",

6: """正確答案：D

【疾病重點】急性肝衰竭（Acute Hepatic Failure）vs. 急性膽管炎（Acute Cholangitis）
- 檢查結果：AST 478、ALT 356（顯著升高）、ALP僅102（輕微升高）、INR 3.1（凝血障礙）
- 此模式：hepatocellular pattern（肝細胞損傷型）→ 可能為肝炎/肝衰竭
- 急性膽管炎：膽管阻塞 → ALP、γ-GT明顯升高，腹部超音波應見膽管擴張
- 此患者：ALP僅輕微升高 + 意識不清 + 黃疸 → 更符合肝細胞性黃疸（肝炎、肝衰竭）
- 「最可能病因為急性膽管炎」→ 與ALP不高、無膽管擴張的表現不符 → D錯誤

【解題關鍵】題目詢問何者「錯誤」。AST/ALT顯著升高但ALP正常 → hepatocellular pattern，不符合膽管炎（膽管阻塞型）表現（選項D）。""",

7: """正確答案：C

【疾病重點】肝細胞癌（HCC）的治療
- <5cm單發性HCC：手術切除可達根治效果 → A正確
- <3cm單發性HCC：射頻消融（RFA）治療成效良好 → B正確
- 多發性HCC的TACE：可改善整體存活率（多項RCT證實），不是「只增加死亡率」→ C錯誤
- 術後追蹤：腹部超音波+AFP定期追蹤 → D正確

【解題關鍵】題目詢問何者「錯誤」。TACE（肝動脈化學栓塞術）對於多發性HCC有姑息治療效果，可延長存活，選項C的「只增加死亡率」說法錯誤。""",

8: """正確答案：D

【疾病重點】狼瘡腎炎（Lupus Nephritis）的評估與治療
- 蛋白尿3.2g/day + 血尿（RBC 50-75/HPF）+ 肌酸酐在3個月內倍增 → 狼瘡腎炎活化
- 腎切片：最可能為Class IV（瀰漫增生性腎絲球腎炎）→ A正確
- 治療：pulse steroid + cyclophosphamide（pulse給法可減少累積毒性）→ B、C正確
- Anti-dsDNA抗體：其濃度與狼瘡腎炎活性高度相關（升高 = 活化）→ D錯誤

【解題關鍵】題目詢問何者「錯誤」。Anti-dsDNA抗體可作為狼瘡腎炎活性的重要指標（濃度越高 = 疾病越活躍），選項D的否定說法錯誤。""",

9: """正確答案：C

【疾病重點】C型肝炎相關腎病（HCV-associated Nephropathy）
- HCV + 腎病症候群（蛋白尿5g、白蛋白2.4）+ 補體下降 → 冷凝球蛋白血症（cryoglobulinemia）合併MPGN
- 腎臟穿刺：最可能為MPGN（Type I）→ D正確
- 冷凝蛋白常見：HCV相關冷凝球蛋白血症 → B正確
- 腎靜脈栓塞（不是腎動脈）：腎病症候群患者因高凝狀態可發生腎靜脈血栓
- 腎動脈栓塞：較少見 → C「較易出現腎動脈栓塞」錯誤（應為腎靜脈栓塞）

【解題關鍵】題目詢問何者「錯誤」。腎病症候群的高凝狀態主要導致腎靜脈血栓，而非腎動脈栓塞（選項C）。""",

10: """正確答案：D

【疾病重點】乾癬性關節炎（Psoriatic Arthritis）
- 乾癬症（psoriasis）病史7年後，出現：
  - 指頭腫脹（sausage digits/dactylitis）
  - 遠端指間關節（DIP）發炎
  - 指甲增厚易脆（nail changes）
- 此組合為乾癬性關節炎的典型表現
- RA通常影響MCP/PIP，不影響DIP；OA影響DIP但無指頭腫；黴菌感染不造成關節炎

【解題關鍵】乾癬症病史 + DIP關節炎 + 香腸指（dactylitis）+ 指甲病變 → 乾癬性關節炎（選項D）。""",

11: """正確答案：A

【疾病重點】出血時間延長的鑑別 — Coumadin vs. Heparin vs. 肝病 vs. vWD
- PT（INR）3.5（延長）+ aPTT 26"（正常，對照27"）→ 只有外因性凝血路徑（PT）延長
- 凝血因子II、VII、IX、X、蛋白C、S：維生素K依賴性
- Warfarin（coumadin）：抑制維生素K依賴性凝血因子 → PT延長，aPTT可正常（早期）→ A
- Heparin：主要延長aPTT（不是PT）→ B不符
- 肝病：PT和aPTT均延長 → C不符
- vWD：aPTT延長或正常，出血時間延長 → D不符

【解題關鍵】PT/INR單獨延長而aPTT正常 → 提示Coumadin（warfarin）治療中（選項A）。""",

12: """正確答案：A

【疾病重點】NSCLC合併EGFR突變的治療
- 40歲亞裔女性、不吸菸、NSCLC Stage IV、EGFR exon 19 deletion → 最佳一線治療為EGFR-TKI
- EGFR-TKI（gefitinib、erlotinib、osimertinib）：顯著優於化療，PFS和OS均改善
- 不需加化療：EGFR突變陽性者，TKI單獨療效已足夠
- 血管增生抑制抗體（bevacizumab）：可作為附加治療但非標準一線

【解題關鍵】EGFR突變陽性NSCLC的一線標準治療為EGFR-TKI單獨使用（選項A）。這是精準醫療的典型案例。""",

13: """正確答案：A

【疾病重點】氣喘（Asthma）的重點知識
- 吸入型類固醇（ICS）：廣泛使用是近年氣喘死亡率下降的主要原因之一 → A正確
- 氣喘定義：實際上難以達成共識，且診斷與其他疾病（如COPD）可能重疊 → B錯誤
- 氣喘氣道發炎：主要為嗜酸性球（eosinophils）、T淋巴球、肥胖細胞浸潤，而非中性球+B淋巴球 → C錯誤
- 控制不良主因：ICS不規則使用（非SABA）→ D錯誤

【解題關鍵】題目詢問何者「正確」。ICS的廣泛推廣使氣喘死亡率明顯下降，選項A正確。""",

14: """正確答案：C

【疾病重點】產後甲狀腺功能低下（Postpartum Hypothyroidism）
- 產後2個月，體重增加、倦怠、怕冷、便秘、皮膚乾燥、血壓升高、心跳60→ 甲狀腺功能低下
- 哺乳中：Hashimoto's thyroiditis或產後甲狀腺炎常見
- 最具診斷價值：free T4 + hsTSH（高敏感TSH）→ C
- 低T4 + 高TSH → 原發性甲狀腺功能低下確診

【解題關鍵】產後出現代謝下降症狀（怕冷、便秘、皮膚乾燥、體重增加）+ 血壓升高 → 甲狀腺功能低下 → 最有診斷價值的檢查為free T4 + hsTSH（選項C）。""",

15: """正確答案：A

【疾病重點】恙蟲病（Scrub Typhus）
- 旅遊史（蘭嶼）+ 膕窩結痂病灶（eschar）+ 發燒 + 皮疹 + 肝功能異常（ALT升高）
- 恙蟲病：Orientia tsutsugamushi（立克次體），由恙蟲（chigger mite）叮咬傳播
- 特徵性表現：焦痂（eschar）→ 強烈提示恙蟲病（診斷90%以上特異性）
- 台灣：蘭嶼、綠島、澎湖為高流行區
- 治療：Doxycycline

【解題關鍵】旅遊後發燒 + 結痂（eschar）+ 皮疹 + 肝功能異常 → 恙蟲病（選項A）。焦痂是診斷關鍵，需仔細全身皮膚檢查（腋下、腹股溝、膕窩常見部位）。""",

16: """正確答案：C

【疾病重點】ESBL產酶腸桿菌科細菌（ESBL-E. coli）的治療
- ESBL（廣效乙內醯胺酵素）：水解大多數青黴素類和頭孢菌素（cephalosporin）
- 對第三代cephalosporin（如cefotaxime）：ESBL細菌通常具抗藥性
- 治療首選：碳青黴烯（Carbapenem）如imipenem、meropenem、ertapenem
- IV ertapenem（選項C）：Carbapenem，對ESBL有效，且可門診注射治療
- 口服cephalexin（A）、IV cefotaxime（B）：ESBL通常具抗藥性，禁用
- IM gentamicin（D）：胺基苷類，對ESBL有活性，但不作為首選

【解題關鍵】ESBL細菌感染的治療首選為carbapenem類抗生素，IV ertapenem（選項C）為最適當的初期治療。""",

17: """正確答案：A

【疾病重點】呼吸困難（Dyspnea）的原因
- 焦慮（anxiety）：可引起換氣過度（hyperventilation）→ 呼吸困難感受 → A「焦慮不會引起呼吸困難」錯誤
- 呼吸困難為主觀感受 → B正確
- 原因多樣（心衰竭、氣道阻塞等）→ C正確
- 夜間陣發性呼吸困難（PND）：心衰竭的典型症狀 → D正確

【解題關鍵】題目詢問何者「錯誤」。焦慮確實可引起換氣過度和呼吸困難感受，選項A的否定說法錯誤。""",

18: """正確答案：B

【疾病重點】水腫（Edema）的特徵
- 肝硬化水腫：低白蛋白血症 → 膠體滲透壓下降，無頸靜脈曲張（JVD是心臟充血的表現）→ A錯誤
- 單側下肢水腫：靜脈阻塞（DVT）或淋巴阻塞 → B正確
- 腎病症候群（低白蛋白血症）：會引起眼皮/臉部水腫（periorbital edema）→ C錯誤
- 心衰竭水腫：重力依賴性（dependent），從下肢開始 → D錯誤

【解題關鍵】題目詢問何者「正確」。單側下肢水腫（非雙側）最常見原因為靜脈或淋巴阻塞（選項B）。""",

19: """正確答案：C

【疾病重點】醫師憲章（Physician Charter）的三大基本原則
- 2002年ABIM/EFIM共同提出的醫師憲章三大原則：
  1. 病人福祉優先原則（Principle of primacy of patient welfare）
  2. 病人自主原則（Principle of patient autonomy）
  3. 社會正義原則（Principle of social justice）
- 「實證醫學執業原則（evidence-based practice）」：不在三大原則之內

【解題關鍵】題目詢問「不是」醫師憲章基本原則者。Evidence-based practice並非醫師憲章的三大基本原則之一，選項C正確。""",

20: """正確答案：D

【疾病重點】二尖瓣狹窄（Mitral Stenosis）的聽診
- 二尖瓣狹窄的典型心音：
  - 心尖部低沉隆隆聲（low-pitched rumbling mid-diastolic murmur）
  - 開瓣音（opening snap）
  - 第一心音亢進（loud S1）
- 「高音調早期舒張期雜音」（high-pitched early diastolic murmur）：此為主動脈逆流（AR）的特徵
- 二尖瓣狹窄確實合併房顫（B正確）和肺高壓（C正確）

【解題關鍵】題目詢問何者「錯誤」。高音調早期舒張期雜音是主動脈逆流（AR）的特徵，不是二尖瓣狹窄（選項D）。""",

21: """正確答案：A

【疾病重點】頸靜脈壓（JVP）的測量
- 測量JVP：以右「內」頸靜脈（internal jugular vein）最準確
  - 右外頸靜脈（external jugular vein）：易受頸部位置影響，較不可靠
- 「a」波：心房收縮（atrial contraction）→ B正確
- 「c」波：三尖瓣關閉（右心室等容收縮期）→ C正確
- 三尖瓣逆流：「v」波變大（右心房被動充填+逆流）→ D正確

【解題關鍵】題目詢問何者「錯誤」。JVP應以右內頸靜脈（不是外頸靜脈）測量最準確（選項A）。""",

22: """正確答案：C

【疾病重點】二尖瓣脫垂（Mitral Valve Prolapse, MVP）
- 病理變化：myxomatous degeneration，好發後葉（posterior leaflet）→ A正確
- Marfan syndrome：結締組織病變，MVP較常見 → B正確
- 好發族群：年輕女性（15-30歲）→ C錯誤（不是男性）
- 大多數無症狀，無需特別治療 → D正確

【解題關鍵】題目詢問何者「錯誤」。MVP好發於年輕女性，而非男性（選項C）。""",

23: """正確答案：A

【疾病重點】STEMI急性期治療的禁忌
- Aspirin 160-325mg：無禁忌應給 → B正確
- 舌下Nitroglycerin：無低血壓或PDE-5抑制劑使用可給 → C正確
- β-blocker：無禁忌可給（IV或口服）→ D正確
- 短效Dihydropyridine CCB（如nifedipine）：急性心肌梗塞禁忌
  - 原因：反射性心搏過速、可能增加梗塞範圍
  - Verapamil/diltiazem：雖為CCB，但在急性STEMI也應避免

【解題關鍵】題目詢問何者「錯誤」。短效dihydropyridine CCB在STEMI急性期禁忌使用（選項A）。""",

24: """正確答案：A

【疾病重點】心臟瓣膜手術死亡率比較
- 主動脈瓣置換手術死亡率：約1-3%
- 二尖瓣置換手術死亡率：約3-6%（通常高於主動脈瓣）
- 「主動脈瓣比二尖瓣死亡率高」→ A錯誤
- 瓣膜+CABG（冠狀動脈繞道）：死亡率比單純瓣膜手術高 → B正確
- 多瓣膜置換：比單瓣膜死亡率高 → C正確
- 二尖瓣修補（repair）比置換（replacement）死亡率低 → D正確

【解題關鍵】題目詢問何者「錯誤」。二尖瓣置換手術的死亡率通常高於主動脈瓣置換，選項A說反了。""",

25: """正確答案：C

【疾病重點】Mallory-Weiss撕裂傷
- 大量飲酒後嘔吐 → 食道-胃交接處（esophagogastric junction）黏膜撕裂 → 出血
- 胃鏡：食道胃交接處縱向裂傷（linear laceration），止血夾治療
- 與食道靜脈曲張鑑別：靜脈曲張呈串珠狀突起，Mallory-Weiss為線形裂傷

【解題關鍵】飲酒後嘔吐 + 食道胃交接處出血 + 胃鏡見裂傷 → Mallory-Weiss tear（選項C）。""",

26: """正確答案：C

【疾病重點】膽酸（Bile Acid）的生理
- 膽酸由肝臟合成 → B正確（不能從食物獲取 → A正確）
- 膽酸的腸肝循環：95%在末端迴腸（terminal ileum）主動再吸收，不是空腸 → C錯誤
- PBC（原發性膽道肝硬化）：膽酸分泌障礙 → 脂肪吸收不良（steatorrhea）→ 脂溶性維生素（A、D、E、K）和鈣吸收不良 → D正確

【解題關鍵】題目詢問何者「錯誤」。膽酸絕大部分在末端迴腸（terminal ileum）再吸收，不是空腸（jejunum）→選項C。""",

27: """正確答案：D

【疾病重點】猛爆性肝炎（Fulminant Hepatitis）的常見原因
- 常見原因：
  - 藥物（如acetaminophen過量、抗結核藥物）→ A
  - A型肝炎（尤其成年人）→ B
  - B型肝炎（急性或急性惡化）→ C
  - 其他：Wilson's disease、自體免疫肝炎、Budd-Chiari syndrome
- 「熬夜」：不是猛爆性肝炎的已知原因 → D不包含

【解題關鍵】題目詢問「不包括」的原因。熬夜不是猛爆性肝炎的常見病因（選項D）。""",

28: """正確答案：A

【疾病重點】H. pylori相關消化道疾病
- H. pylori確認相關：萎縮性胃炎（B）、B細胞胃淋巴瘤/MALT淋巴瘤（C）、十二指腸潰瘍（D）
- 胃食道逆流（GERD）：H. pylori與GERD的關係複雜，甚至有研究顯示H. pylori根除後GERD症狀加重
- 目前共識：H. pylori「不是」胃食道逆流的致病因子（甚至可能有保護作用）→ A除外

【解題關鍵】題目詢問何者「除外」（不是H. pylori的致病疾病）。胃食道逆流不是H. pylori的相關疾病（選項A）。""",

29: """正確答案：C

【疾病重點】原發性膽道性肝硬化（Primary Biliary Cirrhosis/Cholangitis, PBC）的診斷
- 中年女性、茶色尿、皮膚搔癢、膽汁淤積型黃疸（ALP 586，顯著升高）、HBsAg陰性、anti-HCV陰性
- 高度懷疑PBC：anti-mitochondrial antibody（AMA，M2型）為主要診斷抗體 → B需要檢查
- 腹部超音波：排除膽道阻塞 → A需要
- 血清銅藍蛋白（ceruloplasmin）：排除Wilson's disease → C適宜
- γ-GT：在已知ALP明顯升高的情況下，γ-GT增加的診斷價值「最小」

【解題關鍵】ALP已大幅升高，γ-GT（選項D）的額外診斷價值有限，為「最不適宜」的額外檢查。(答案C為血清銅藍蛋白其實是需要的排除診斷，但依據答案key=C，本題有爭議，以答案鍵C為準)""",

30: """正確答案：C

【疾病重點】Ranson準則（Ranson's Criteria）用於急性胰臟炎嚴重度評估
- Ranson準則（48小時評估項目）：
  1. 血比容（Hct）下降 >10%
  2. 動脈血氧（PaO₂）< 60 mmHg
  3. 血清鈣（Ca）< 8 mg/dL
  4. BUN升高 >5 mg/dL
  5. 鹼基過剩（Base deficit）> 4 mEq/L
  6. 液體積聚 >6L
- 血清鉀（serum potassium）：不在Ranson準則之列 → C為非計分項目

【解題關鍵】Ranson 48小時評估項目包含Hct、PaO₂、血鈣、BUN等，但不包括血清鉀（選項C）。""",

31: """正確答案：C

【疾病重點】末期腎病（ESRD）的最佳治療
- 腎臟替代療法比較：
  - 血液透析（HD）：最常用，但需每週3次8-12小時
  - 腹膜透析（PD）：在家可進行，但長期溶質清除效果略差
  - 腎臟移植：移植後生活品質最佳、存活率最高、長期最佳治療 → C
  - 血液過濾透析：無特別優勢

【解題關鍵】腎臟移植（kidney transplantation）是末期腎病的最佳治療（treatment of choice），可最大程度改善生活品質和長期存活（選項C）。""",

32: """正確答案：D

【疾病重點】原發性醛固酮症（Primary Aldosteronism / Conn's Syndrome）
- 夜尿、高血壓（150/94）、低鉀血症（K 2.8）、代謝性鹼中毒（HCO₃⁻ 30）、尿鉀排泄高（50 mmol/day）
- 低鉀 + 尿鉀排泄增加（> 20-25 mmol/day）→ 腎性鉀流失
- 高血壓 + 低鉀 + 代謝性鹼中毒 → 原發性醛固酮症
- 鑑別：Bartter syndrome（血壓正常）、RTA（無低鉀血症或無代謝鹼）

【解題關鍵】高血壓 + 低鉀血症 + 代謝性鹼中毒 + 尿鉀增加 → 原發性醛固酮症（選項D）。確診需測血漿醛固酮/腎素比值（ARR）。""",

33: """正確答案：C

【疾病重點】C型肝炎相關腎病變的類型（最少見者）
- HCV相關腎病常見類型（由多到少）：
  1. 冷凝球蛋白腎小球腎炎（cryoglobulinemic GN）→ 最常見
  2. 第一型MPGN（membranoproliferative GN）→ 常見
  3. 膜性腎病變（membranous GN）→ 較少
  4. 急性腎間質腎炎（acute interstitial nephritis）→ 最少見
- 急性腎間質腎炎與HCV的關聯性最低 → C最少見

【解題關鍵】題目詢問HCV腎病中「最少見」的類型。急性腎間質腎炎（acute interstitial nephritis）與HCV的直接關聯性最低（選項C）。""",

34: """正確答案：C

【疾病重點】腎絲球性血尿（Glomerular Hematuria）的鑑別
- 腎絲球性血尿的特徵：尿液紅血球形態異常（dysmorphic RBCs）
  - 最具特徵：棘形紅血球（acanthocytes/echinocytes）
  - 相位差顯微鏡（phase contrast microscopy）
- 血清肌酸酐（A）：反映腎功能，不直接鑑別血尿來源
- 血清補體C3（B）：可提示補體激活型腎炎，但非鑑別血尿來源
- IVU（D）：可看結構，不鑑別細胞形態

【解題關鍵】鑑別腎絲球性vs.非腎絲球性血尿，最重要的檢查是尿液紅血球形態（dysmorphic RBCs，選項C）。""",

35: """正確答案：C

【疾病重點】僵直性脊椎炎（Ankylosing Spondylitis, AS）與HLA-B27
- HLA-B27陽性 vs. AS：一般人中HLA-B27陽性者，約1-5%會發展為AS（不是20%）→ C錯誤
- HLA-B27陽性者較B27陰性者，葡萄膜炎更常見 → A正確
- HLA-B27陽性者家族傾向較高 → B正確
- 北美印第安人HLA-B27盛行率可達50%（遠高於台灣原住民的3-9%）→ D正確

【解題關鍵】題目詢問何者「錯誤」。HLA-B27陽性者中只有約1-5%會發展AS，選項C「20%」的數字錯誤。""",

36: """正確答案：C

【疾病重點】磷灰石晶體沉積症（Apatite Crystal Deposition Disease / Calcific Tendinitis）
- 右肩劇痛 + subdeltoid bursa壓痛 + 尿酸8.0（輕微升高，非確診痛風）+ X光/MRI見鈣化
- Apatite晶體（hydroxyapatite）：好發肩峰下滑液囊（subdeltoid/subacromial bursa）
- 痛風：尿酸必須更高且關節液見尿酸鹽晶體（negatively birefringent）
- RA：對稱多關節，RF 30（輕微升高，非診斷性）
- 冰凍肩：ROM受限但無X光鈣化

【解題關鍵】肩部鈣化 + subdeltoid bursa壓痛 + X光/MRI鈣化影像 → 磷灰石晶體關節炎（選項C）。""",

37: """正確答案：A

【疾病重點】狼瘡腎炎（Lupus Nephritis）的藥物選擇
- 蛋白尿2g/day + 腎功能不足（creatinine 2.0 mg/dL）
- Cyclosporine（A）：具腎毒性（nephrotoxic），腎功能不足時禁用 → 最不適用
- Leflunomide（B）：可用於SLE，腎功能輕度不足時需調整
- Rituximab（C）：抗CD20，可用於難治性狼瘡腎炎
- Mycophenolate mofetil（D）：MMF，是狼瘡腎炎的標準免疫抑制劑

【解題關鍵】Cyclosporine有腎毒性，在已有腎功能不全（Cr 2.0）的狼瘡腎炎患者中「最不適用」（選項A）。""",

38: """正確答案：D

【疾病重點】修格蘭氏症候群（Sjögren's Syndrome）的血清學
- 乾眼 + 乾口 + 腮腺腫脹 + 關節炎 → 修格蘭氏症候群
- 常見陽性抗體：RF（A）、ANA（B）、Anti-SS-A/Ro和Anti-SS-B/La（C）
- 「最不會」出現陽性：抗心磷脂抗體（anticardiolipin antibody）→ D
  - Anticardiolipin/antiphospholipid：為SLE或抗磷脂症候群的特徵，非Sjögren's特徵

【解題關鍵】題目詢問在修格蘭氏症候群中「最不會陽性」的抗體。Anticardiolipin抗體（選項D）與Sjögren's無特異性關聯。""",

39: """正確答案：B

【疾病重點】化療期間細菌感染的最高風險情況
- 化療導致中性球低下（neutropenia）是細菌感染的最重要危險因子
- 定義：絕對中性球計數（ANC）< 500/μL → Febrile neutropenia
- ANC < 500/μL：感染風險急劇上升，尤其是革蘭氏陰性桿菌和皮膚菌叢
- Corticosteroid（A）：雖增加感染風險，但不如neutropenia顯著
- 貧血（Hb < 7，C）和體重減輕（D）：不是細菌感染的直接危險因子

【解題關鍵】化療期間細菌感染最常見於中性球計數 < 500/μL的情況（選項B）。""",

40: """正確答案：D

【疾病重點】鼻咽癌（Nasopharyngeal Carcinoma, NPC）的診斷評估
- 流鼻血 + 左側頸部固定無痛性腫塊 → 高度懷疑鼻咽癌頸部淋巴轉移
- 鼻咽癌好發：亞裔（尤其廣東人/台灣人）、EBV相關
- 診斷流程：纖維鼻咽喉鏡（fiberoscopic examination）+ 鼻咽部切片（nasopharyngeal biopsy）→ D
- 切除生檢（B）：頸部腫塊不建議直接切除，可能破壞淋巴結完整性影響分期
- FNA（C）：可作為初步評估，但最終仍需鼻咽部切片確診

【解題關鍵】疑似鼻咽癌應行纖維鼻咽喉鏡檢查 + 鼻咽部切片（選項D），這是診斷鼻咽癌的標準流程。""",

41: """正確答案：B

【疾病重點】T細胞淋巴母細胞淋巴瘤/白血病（Precursor T-cell Lymphoblastic Lymphoma/Leukemia）
- 18歲男性 + 頸部淋巴腫大 + 前縱隔腫塊（胸部X光）+ 輕度血細胞下降 + blast 2%
- 前縱隔腫塊（anterior mediastinal mass）+ 青少年/年輕男性 → 強烈提示T-cell lymphoblastic lymphoma
- T-cell ALL/LBL：好發前縱隔，可侵犯骨髓（blast）和周邊血
- B-cell ALL：不好發前縱隔
- Burkitt's：常見腹部腫塊
- Adult T-cell lymphoma：HTLV-1相關，好發成年人

【解題關鍵】年輕男性 + 前縱隔腫塊 → Precursor T-cell lymphoblastic lymphoma/leukemia（選項B）。""",

42: """正確答案：B

【疾病重點】低分子量肝素（LMWH）的特性
- 劑量可依體重決定 → A正確
- 監測LMWH：不使用aPTT（LMWH對aPTT影響較小，且相關性差）→ B錯誤
  - LMWH監測：用Factor Xa activity（anti-Xa level）→ C正確
- LMWH主要由腎臟代謝，腎功能不全需調整劑量 → D正確

【解題關鍵】題目詢問何者「錯誤」。LMWH「不能」用aPTT監測（選項B），監測應使用anti-Factor Xa activity。""",

43: """正確答案：C

【疾病重點】慢性骨髓性白血病（CML）的一線治療
- 32歲男性、WBC 120,000/μL、嗜鹼球（basophil）5%、骨髓染色體t(9;22)（Philadelphia chromosome）→ CML
- 第一線治療（當前共識）：酪氨酸激酶抑制劑（TKI，如imatinib/Gleevec）→ C
- Hydroxyurea（A）：舊時代，非根治，現已非首選
- IFN-alpha（B）：TKI前時代使用，現已被取代
- 異體造血幹細胞移植（D）：非一線（保留給TKI失敗或特定高危患者）

【解題關鍵】CML一線治療為酪氨酸激酶抑制劑（TKI，選項C），如imatinib，具高效且耐受性佳。""",

44: """正確答案：B

【疾病重點】急性骨髓性白血病（AML）的危險因子
- AML危險因子：
  - 唐氏症（Down syndrome）→ A（增加風險）
  - 苯（Benzene）職業暴露 → C（增加風險）
  - 曾使用拓撲異構酶II抑制劑（如etoposide）→ D（t-AML）
  - 放射線、MDS、再生不良性貧血等
- 類風濕性關節炎（RA）：不增加AML風險
  - 注意：RA治療的某些藥物（如alkylating agent）可能增加風險，但RA本身不直接增加AML

【解題關鍵】題目詢問「不會」增加AML風險者。類風濕性關節炎本身不增加AML發生機率（選項B）。""",

45: """正確答案：B

【疾病重點】多發性骨髓瘤高鈣血症（Hypercalcemia in Multiple Myeloma）的治療
- 多發性骨髓瘤高鈣血症機轉：骨髓瘤細胞活化破骨細胞 → 骨骼溶解 → Ca²⁺釋放
- 有效治療：
  - 雙磷酸鹽（Bisphosphonate）：抑制破骨細胞 → A有效
  - 類固醇（Corticosteroid）：抑制骨髓瘤細胞及破骨細胞 → C有效
  - 降鈣素（Calcitonin）：抑制破骨細胞活性，快速但短效 → D有效
- 氟化物（Fluoride）：增加骨密度，但「不治療」高鈣血症 → B無效

【解題關鍵】題目詢問「不能達到治療目的」者。氟化物（fluoride）不用於治療高鈣血症（選項B）。""",

46: """正確答案：A

【疾病重點】支氣管擴張症（Bronchiectasis）的治療
- 長期預防性抗生素：「對反覆感染患者長期使用抗生素以防止進一步破壞」→ 此說法過於絕對且有爭議
  - 實際：長期抗生素（如azithromycin）適用於特定患者（頻繁急性惡化），但非所有患者
  - 「應長期使用」為過度廣泛的錯誤建議 → A錯誤
- 支氣管擴張劑：改善症狀 → B正確
- 肺部復健/胸腔物理治療：清除痰液 → C正確
- Aspergilloma引起咳血：可手術切除 → D正確

【解題關鍵】題目詢問何者「錯誤」。並非所有反覆感染的支氣管擴張症患者都應長期使用抗生素（選項A）。""",

47: """正確答案：A

【疾病重點】呼吸器 Volume-cycled 模式下降低吸氣流量（Flow Rate）的效應
- Volume-cycled（容積控制）模式：每次送出固定潮氣容積（VT）
- 降低吸氣流量，其他設定不變：
  - 要送相同的VT，但流量慢了 → 需要更長的時間 → 吸氣時間（Ti）延長 → A正確
  - VT不變（由volume cycling決定）→ B不對
  - 尖峰吸氣壓（PIP）：流量低 → 管路阻力造成的壓力降低 → PIP反而可能降低 → C不對
  - 呼吸次數（RR）：由設定決定，不變 → D不對

【解題關鍵】降低吸氣流量時（VT不變），需要更長的時間送入相同容積 → 吸氣時間（Ti）延長（選項A）。""",

48: """正確答案：C

【疾病重點】ARDS呼吸器設定調整 — 呼吸性鹼中毒的處理
- 血液氣體：pH 7.50（鹼）、PaCO₂ 22（極低）→ 呼吸性鹼中毒
- 機制：過度換氣（hyperventilation）→ 過多CO₂呼出
- 呼吸器設定：VT 660mL（60kg患者 → 11 mL/kg，遠超ARDS保護性通氣建議6 mL/kg）
- 解決呼吸性鹼中毒：減少分鐘通氣量 → 最佳方法：減少潮氣容積（VT）→ C
  - 同時符合ARDS保護性通氣（lung-protective ventilation）原則

【解題關鍵】ARDS患者PaCO₂過低（呼吸性鹼中毒），且VT過大（11 mL/kg），最適當的調整是減少潮氣容積（選項C）。""",

49: """正確答案：D

【疾病重點】滲出性肋膜積液（Exudative Pleural Effusion）的原因
- Light's criteria判斷滲出液（exudate）：
  1. 肋膜液/血清蛋白比 > 0.5
  2. 肋膜液/血清LDH比 > 0.6
  3. 肋膜液LDH > 2/3正常上限
- 常見滲出液原因：肺炎（A）、惡性腫瘤（B）、胰臟炎（C）、結核病、膠原血管疾病
- 心臟衰竭：最常見「漏出液（transudate）」原因 → D不是滲出液常見原因

【解題關鍵】題目詢問「不是」滲出性肋膜積液的常見原因。心臟衰竭造成漏出液，不是滲出液（選項D）。""",

50: """正確答案：C

【疾病重點】EGFR基因突變高風險族群
- EGFR突變在肺癌中的流行病學特徵：
  ①女性：較男性高 ✓
  ②腺癌（adenocarcinoma）：較鱗癌等高 ✓
  ③抽菸：吸菸者EGFR突變率較低 ✗（吸菸為KRAS突變高危）
  ④亞洲人種：EGFR突變率40-50%，遠高於西方人（10-15%）✓
  ⑤小細胞癌：EGFR突變率極低 ✗
- 正確組合：①②④ → C

【解題關鍵】EGFR突變高風險：女性、腺癌、亞洲人、不吸菸者。選項C（①②④）正確。""",

51: """正確答案：D

【疾病重點】ARDS的低潮氣容積+高PEEP通氣策略
- 目的：
  - 減少barotrauma（氣壓傷）→ A是目的
  - 減少吸入高氧濃度的時間（減少O₂毒性）→ B是目的
  - 減少死亡率（ARDSNet研究證實）→ C是目的
- 「減少呼吸器引發的感染（ventilator-associated pneumonia）」：
  - 低VT + 高PEEP的主要目的「不是」減少VAP
  - VAP預防靠束帶式照護（bundle care）、床頭抬高等

【解題關鍵】題目詢問何者「不是」低VT/高PEEP的目的。減少呼吸器相關感染（VAP）不是此通氣策略的主要目標（選項D）。""",

52: """正確答案：A

【疾病重點】Kallmann症候群（Kallmann Syndrome）
- 臂展 > 身高（類宦官體型，eunuchoid proportions）+ 陰莖短小 + 無陰毛 + 嗅覺不佳
- Kallmann syndrome：低促性腺激素型性腺功能低下（hypogonadotropic hypogonadism）+ 嗅覺喪失
- 特徵：睪丸小而軟（發育不全）→ A正確
- 47XXY（B）：Klinefelter syndrome（有雄性化發育，嗅覺正常）
- 矮小三角臉（C）：Turner syndrome（女性）
- 重度肥胖智障（D）：Prader-Willi syndrome

【解題關鍵】類宦官體型 + 嗅覺不佳 + 性腺發育不全 → Kallmann syndrome → 睪丸小而軟（選項A）。""",

53: """正確答案：C

【疾病重點】泌乳素瘤（Prolactinoma）— 大腺瘤（Macroadenoma, >1 cm）
- 閉經 + 泌乳 + 1.5cm腦垂腺腫瘤 → 泌乳素瘤大腺瘤
- 不治療 → 低雌激素 → 骨質疏鬆 → A正確
- 向上壓迫視交叉 → 視野缺損（bitemporal hemianopia）→ B正確
- Sulpiride（舒比利）：為多巴胺拮抗劑 → 增加泌乳素分泌 → 禁用 → C錯誤
  - 治療應用多巴胺促進劑（bromocriptine、cabergoline）
- 手術成功率與腫瘤大小呈負相關（腫瘤越大越難全切）→ D正確

【解題關鍵】題目詢問何者「錯誤」。Sulpiride是多巴胺拮抗劑，會使泌乳素上升，是治療泌乳素瘤的禁忌（選項C）。""",

54: """正確答案：B

【疾病重點】梨狀竇瘻管（Pyriform Sinus Fistula）
- 18歲女性、左頸部急性發炎（紅腫熱痛）+ 發燒 → 頸部感染
- 年輕人反覆左頸部感染 → 高度懷疑先天梨狀竇瘻管（pyriform sinus fistula）
  - 先天異常，多在左側
  - 反覆發作的頸部蜂窩組織炎或膿瘍
  - 感染通道經由梨狀竇（pyriform sinus）
- 亞急性甲狀腺炎（A）：頸部疼痛，但甲狀腺區域
- 甲狀腺舌管囊腫（C）：中線，感染時也可紅腫
- 未分化甲狀腺癌（D）：老年人，快速生長腫塊

【解題關鍵】年輕人左頸部反覆感染 → 梨狀竇瘻管（選項B）。這是台灣常見先天頸部異常的考點。""",

55: """正確答案：A

【疾病重點】腦垂腺放射線治療後的激素異常
- 腦垂腺接受放射線後，激素缺乏的發生順序（由早到晚，由最敏感到最不敏感）：
  1. 生長激素（GH）：最早、最常出現 → A
  2. 促性腺激素（LH/FSH）
  3. 促甲狀腺素（TSH）
  4. 促腎上腺皮質素（ACTH）：最晚出現
- 泌乳素（PRL）：放射線後可能升高（因多巴胺抑制受損）

【解題關鍵】腦垂腺放射線治療後「最早/最常」出現的激素缺乏為生長激素（GH，選項A）。""",

56: """正確答案：C

【疾病重點】庫欣氏症候群（Cushing's Syndrome）的最常見原因
- Cushing's syndrome病因（由常到罕）：
  1. 外源性類固醇過量使用（iatrogenic）→ 臨床最常見 → C
  2. 腦垂腺ACTH腺瘤（Cushing's disease）→ 內因性最常見
  3. 腎上腺皮質腫瘤
  4. 異位ACTH分泌（小細胞肺癌、胸腺癌）
- 胸腺腫瘤（D）：極少見

【解題關鍵】臨床上最常見的庫欣氏症候群原因為外源性類固醇過量使用（iatrogenic steroid use，選項C）。""",

57: """正確答案：B

【疾病重點】第二型糖尿病（Type 2 DM）治療 — 錯誤陳述
- HbA1c目標 <7%：一般治療目標 → A正確
- Sulfonylurea作為第一線用藥 → B錯誤（目前第一線為Metformin，非sulfonylurea）
- DPP-4抑制劑提高餐後GLP-1濃度：正確機轉（DPP-4分解GLP-1，抑制DPP-4 → GLP-1上升）→ C正確
- α-glucosidase抑制劑降低餐後血糖：正確機轉（抑制腸道碳水化合物分解）→ D正確

【解題關鍵】題目詢問何者「錯誤」。第二型糖尿病的口服藥物第一線治療為Metformin，非sulfonylurea（選項B）。""",

58: """正確答案：A

【疾病重點】感染性心內膜炎的預防性抗生素適應症
- AHA指引：牙科手術前預防性抗生素的適應症（高風險瓣膜病變）：
  - 人工心臟瓣膜 → B需要
  - 有心內膜炎病史 → C需要
  - 心臟移植後有瓣膜病變 → D需要
  - 先天性心臟病（特定類型）
- 「二尖瓣脫垂但無逆流」：低風險，不需要預防性抗生素 → A不需要

【解題關鍵】題目詢問「不需要」預防性抗生素者。MVP without MR（二尖瓣脫垂無逆流）不在AHA心內膜炎預防性抗生素的適應症（選項A）。""",

59: """正確答案：D

【疾病重點】麻疹（Measles）
- 1歲女嬰：發燒 + 咳嗽 + 流鼻水 + 結膜炎（三C：cough, coryza, conjunctivitis）
- 發燒後3-4天出現柯氏斑點（Koplik's spots）：口腔黏膜的鹽粒狀白斑，為麻疹特徵性前驅症狀
- 之後出現麻疹斑丘疹（從臉部向下蔓延）
- 玫瑰疹（roseola）：6-18月，突然高燒退後出疹，無前驅症狀
- 猩紅熱：草莓舌，鏈球菌感染後
- 川崎氏症：草莓舌、冠狀動脈瘤、眼球充血

【解題關鍵】三C（咳嗽、鼻炎、結膜炎）+ Koplik's spots + 發燒後3-4天出疹 → 麻疹（選項D）。""",

60: """正確答案：B

【疾病重點】微生物與癌症的關聯性
- H. pylori → 胃癌（gastric adenocarcinoma）：強烈相關 → A高關聯
- HPV → 子宮頸癌（cervical cancer）：非常強烈相關；但「子宮癌（uterine/endometrial cancer）」主要與肥胖、雌激素相關，非HPV → B低關聯
- HHV-8 → Kaposi's sarcoma：直接相關 → C高關聯
- EBV → Hodgkin's lymphoma（尤其混合細胞型）：強相關 → D高關聯

【解題關鍵】題目詢問「關聯性最低」者。HPV與「子宮癌（子宮體癌/endometrial）」關聯最低（HPV主要與子宮頸癌相關，選項B）。""",

61: """正確答案：A

【疾病重點】西尼羅病毒（West Nile Virus, WNV）感染
- 傳播方式：主要由受感染蚊子（Culex species）叮咬傳播
- 宿主（reservoir）：鳥類（birds）
- 媒介（vector）：蚊子（mosquito）
- 「鳥類是主要傳染媒介（vector）」→ A錯誤（鳥類是宿主/reservoir，不是vector）
- 大多數感染無症狀（80%）→ B正確
- 嚴重症狀：腦炎、腦膜炎（神經侵襲性疾病）→ C正確
- 肝炎：偶有報告 → D正確

【解題關鍵】題目詢問何者「最不適當」。鳥類是WNV的宿主（reservoir），不是傳染媒介（vector）→選項A。蚊子才是vector。""",

62: """正確答案：D

【疾病重點】各腹瀉病原菌的最低感染劑量（Infectious Dose）
- 感染劑量由低（高毒力）到高（低毒力）：
  - Shigella：<100個菌（極低）→ A
  - E. histolytica：10-100個囊孢 → B
  - Giardia lamblia：10-25個囊孢 → C
  - Vibrio cholerae：需要10⁸以上（極大量）→ D（需最大劑量）
- Vibrio cholerae需要大量細菌才能致病，因為胃酸可殺滅大多數

【解題關鍵】Vibrio cholerae的致病所需菌量最多（>10⁸），為選項中最大量（選項D）。""",

63: """正確答案：D

【疾病重點】抗生素使用的正確知識
- 不當使用抗生素確實增加抗藥性和醫療浪費 → A正確
- 不當使用增加死亡率和副作用 → B正確
- 抗生素選用須考量多重因素（年齡、腎肝功能等）→ C正確
- 「抗生素劑量濃度與抗藥性無關」→ D錯誤
  - 次抑菌濃度（sub-inhibitory concentration）正是促進細菌突變和抗藥性的重要機制
  - 藥物濃度/抗藥性關係是抗生素學的核心概念（PK/PD）

【解題關鍵】題目詢問何者「錯誤」。抗生素劑量/濃度與細菌抗藥性「高度相關」（次抑菌濃度促進突變）→選項D。""",

64: """正確答案：D

【疾病重點】嚴重失溫（Severe Hypothermia）合併心室顫動（VF）的處理
- 體溫26℃ + VF：嚴重失溫
- 失溫合併VF的處理：
  - 立即CPR（不中斷）
  - 嘗試去顫（defibrillation）：若失敗，應繼續CPR同時復溫
  - 反覆去顫（D）：目前指引建議在復溫前後可多次嘗試去顫 → D最合宜
  - 注意：嚴重失溫心臟對去顫的反應性下降，但仍應嘗試

【解題關鍵】失溫VF患者的優先處置為去顫（defibrillation）嘗試並繼續CPR（選項D）。同時應積極復溫。""",

65: """正確答案：A

【疾病重點】嚴重失溫最快復溫方式
- 復溫方式（由快到慢）：
  1. 體外循環（ECMO/cardiopulmonary bypass）→ 最快 → A
  2. 血液透析（HD）→ 較快
  3. 腹膜透析（PD）→ 中等
  4. 溫熱洗胃（gastric lavage）→ 較慢
- 體外循環可同時提供血液動力學支持，是嚴重失溫合併心臟停止的最佳治療

【解題關鍵】嚴重失溫快速復溫的最佳方式為體外循環（cardiopulmonary bypass / ECMO，選項A）。""",

66: """正確答案：D

【疾病重點】生命週期的個體差異性
- 老年族群（elderly）的特點：
  - 生理和社會層面個體間差異最大
  - 原因：累積了一生的不同生活經驗、慢性病、社會條件
  - 老年醫學原則：不能用單一標準治療所有老年人

【解題關鍵】個體間差異性最大的年齡層為老年（選項D）。此為老年醫學的核心概念——老年人異質性（heterogeneity）最高。""",

67: """正確答案：B

【疾病重點】肥胖（Obesity）的相關知識
- 減重可降低血壓（非藥物治療）→ A正確
- 成人肥胖與兒童肥胖「相關」（兒童肥胖成年後更易持續）→ B錯誤
- 肥胖與血脂異常、T2DM、癌症相關 → C正確
- 每日減少500-1000大卡 → 每週減0.5-1公斤 → D正確

【解題關鍵】題目詢問何者「錯誤」。成人肥胖與兒童肥胖「有關」（兒童時期肥胖是成年肥胖的危險因子），選項B的「無關」說法錯誤。""",

68: """正確答案：D

【疾病重點】非典型肺炎（Atypical Pneumonia）— Mycoplasma pneumoniae
- 21歲男性、乾咳漸轉稀痰、全身倦怠、頭痛肌肉痠痛（無喉嚨痛鼻水）+ 室友有類似症狀
- 身體檢查：低肺野crackles、無其他異常
- 非典型肺炎（Mycoplasma、Chlamydia、Legionella）：好發年輕成人、乾咳為主、群聚感染
- 最適當處置：依臨床發現安排胸部X光 → D
  - 不能僅說病毒感染等它好（A）
  - 不用直接給ampicillin（非典型肺炎無效）
  - 不需立即CT（初步用X光即可）

【解題關鍵】年輕人非典型肺炎的初步處置應安排胸部X光（選項D），然後依影像決定抗生素（macrolide或doxycycline）。""",

69: """正確答案：C

【疾病重點】病情告知與知情同意（Informed Consent）
- 患者使用口服類固醇的風險（體重增加、情緒失調、骨頭壞死）→ 醫師應告知
- 正確做法：告知病情風險，由病人自行決定是否繼續服藥 → C（自主原則）
- 不應告知（A）：違反知情同意原則
- 不論氣喘控制與否就減藥（B）：可能危及患者安全
- 不說明理由轉介（D）：違反醫師責任和知情同意

【解題關鍵】知情同意原則：醫師有義務告知治療的風險，並尊重病人的自主決定（選項C）。""",

70: """正確答案：B

【疾病重點】台灣嬰幼兒預防接種時程（11個月大）
- 11個月大兒童應已完成的疫苗（依衛福部建議）：
  ①卡介苗（BCG）：出生時 ✓
  ②B型肝炎（HBV）：出生、1個月、6個月 ✓
  ③白破百（DTaP）：2、4、6個月 ✓
  ④小兒麻痺（IPV/OPV）：2、4個月 ✓
  ⑤水痘：12-15個月 → 尚未到 ✗
  ⑥MMR（麻疹腮腺炎德國麻疹）：12-15個月 → 尚未到 ✗
  ⑦日本腦炎：15個月 → 尚未到 ✗
  ⑧破傷風白喉（Td）：小學一年級 → 尚未到 ✗
- 11個月大已接種：①②③④ → B

【解題關鍵】11個月大嬰兒已接種的疫苗為BCG、HBV、DTaP、IPV（選項B：①②③④）。""",

71: """正確答案：B

【疾病重點】NNH（Number Needed to Harm）計算
- 公式：NNH = 1 / ARI（絕對風險增加量）
- HRT組冠心病年發生率：37/10,000
- 對照組冠心病年發生率：30/10,000
- ARI = 37/10,000 - 30/10,000 = 7/10,000 = 0.0007
- NNH = 1/0.0007 = 10,000/7 ≈ 1428.6 ≈ 1428 → B

【解題關鍵】NNH = 1/ARI = 10,000/7 ≈ 1428（選項B）。每治療1428位接受HRT的女性，才會多出現1例冠心病。""",

72: """正確答案：B

【疾病重點】跨越理論模式（Transtheoretical Model, TTM）的階段
- TTM五階段：
  1. 未考慮期（Precontemplation）：沒有在未來6個月戒菸的計畫
  2. 考慮期（Contemplation）：打算在未來6個月內改變
  3. 準備期（Preparation）：打算在下個月內採取行動
  4. 行動期（Action）：已在改變行為，持續不超過6個月
  5. 維持期（Maintenance）：行為改變已超過6個月
- 「想要在一個月之內採取戒菸行動」→ 準備期（Preparation）
- 選項B（考慮階段）= Preparation stage（依本題選項對應）

【解題關鍵】計劃在一個月內戒菸 = 準備期（選項B）。""",

73: """正確答案：C

【疾病重點】準備期患者的戒菸介入策略
- 準備期（Preparation）患者的介入：
  - 幫助設定明確的戒菸日期（quit date）
  - 提供戒菸資源和計劃
- 各選項的對應階段：
  - A（減少對抽菸的誘惑情感）→ 行動/維持期
  - B（加強認知戒菸好處）→ 考慮期
  - C（鼓勵設定開始戒菸的日期）→ 準備期 ✓
  - D（討論抽菸對健康影響）→ 未考慮/考慮期

【解題關鍵】準備期患者已決定要戒菸，醫師最適當的介入是幫助設定戒菸日期（選項C）。""",

74: """正確答案：D

【疾病重點】急性胰臟炎（Acute Pancreatitis）的影像診斷
- 急性上腹疼痛 + 噁心嘔吐 + CT顯示胰臟腫脹/水腫/周圍積液 → 急性胰臟炎
- CT特徵：胰臟腫大、周圍脂肪層模糊（peripancreatic stranding）、胰臟壞死（無增強）
- 急性胰臟炎診斷標準（Revised Atlanta Classification）：
  1. 典型腹痛
  2. 血清lipase或amylase > 3倍正常上限
  3. CT/MRI典型影像

【解題關鍵】CT顯示胰臟腫脹及周圍積液的典型影像 → 急性胰臟炎（選項D）。""",

75: """正確答案：B

【疾病重點】肝性腦病變（Hepatic Encephalopathy）分期
- West Haven分期：
  - 第一期：輕微認知障礙、睡眠障礙、注意力不集中
  - 第二期：行為改變（personality change）、言語遲緩、嗜睡（drowsiness）、asterixis（撲翼震顫）
  - 第三期：嚴重混亂、昏昏欲睡（stupor）、仍可喚醒
  - 第四期：昏迷（coma）、無法喚醒
- 此患者：行為改變 + 說話變慢 + 嗜睡（drowsiness）→ 第二期

【解題關鍵】行為改變 + 言語遲緩 + 嗜睡 = 肝性腦病變第二期（選項B）。""",

76: """正確答案：D

【疾病重點】深部靜脈栓塞（DVT）的危險因子（Virchow's Triad）
- 靜脈瘀滯（stasis）：臥床、手術、長途旅行
- 血管內皮損傷（endothelial injury）：創傷、手術
- 高凝狀態（hypercoagulability）：癌症、妊娠、口服避孕藥、遺傳性血栓傾向
- 主要危險因子：癌症（A）、肥胖（B）、懷孕（C）→ 均為DVT危險因子
- 糖尿病（D）：不是DVT的主要獨立危險因子（動脈粥樣硬化的危險因子，不是靜脈血栓）

【解題關鍵】題目詢問「較不可能」的DVT危險因子。糖尿病不是DVT的主要危險因子（選項D）。""",

77: """正確答案：C

【疾病重點】心室頻脈（Ventricular Tachycardia, VT）伴血動力學不穩定的處理
- 突發心悸 + 臉色蒼白 + 冒冷汗 + 意識模糊 + 血壓70/30 mmHg → 血動力學不穩定
- 心電圖：寬複合波心搏過速（推測VT）
- 血動力學不穩定VT的治療：同步直流電整流（synchronized cardioversion）→ C
- Adenosine（D）：用於窄複合波SVT，不適用VT
- Atropine（B）：用於心搏過緩
- 頸動脈竇按摩（A）：用於SVT，VT無效

【解題關鍵】血動力學不穩定的心搏過速（可能VT）→ 立即同步電整流（synchronized cardioversion，選項C）。""",

78: """正確答案：A

【疾病重點】旅行者腹瀉（Traveler's Diarrhea）
- 預防性抗生素：不建議常規使用（可增加抗藥性、副作用，且多數腹瀉自癒）→ A錯誤
- 細菌感染（ETEC等）：最常見致病原（約80%）→ B正確
- 治療以補充液體（rehydration）最重要 → C正確
- 大多數感染性腹瀉自限性（self-limited）→ D正確

【解題關鍵】題目詢問何者「錯誤」。預防性抗生素「不應」常規使用於旅行者腹瀉的預防（選項A）。""",

79: """正確答案：A

【疾病重點】台灣醫師法 — 未親自診察不可開藥
- 台灣《醫師法》第11條：醫師非親自診察，不得施行治療、開給方劑或交付診斷書
- 正確做法：說明醫師未親自診察不可開藥而拒絕 → A最符合法律規定
- 選項B/C/D均存在未親自診察即開藥的可能性，違反醫師法

【解題關鍵】台灣醫師法明確規定，醫師須親自診察才能開藥，拒絕代開藥（選項A）為合法且最恰當的作法。""",

80: """正確答案：C

【疾病重點】台灣《醫療法》說明病情的相關規定
- 《醫療法》第81條規定醫療機構（醫師）應向病人說明：
  - 病情
  - 治療方針
  - 處置（手術等）
  - 用藥
  - 預後情形
  - 可能之不良反應
- 選項C完整描述了法定說明內容 → C正確
- A：說明可由護理師等輔助，非限醫師 → A不完全正確
- B：說明對象包括病人或其家屬 → B錯誤
- D：法律未明確要求記錄「時間、地點」 → D過於嚴格

【解題關鍵】台灣《醫療法》第81條規定的說明內容包括：病情、治療方針、處置、用藥、預後及可能不良反應（選項C）。"""
}

def make_key(n):
    return f"民國106年_第2次_醫學(三)_{n}"

with open(NOTES_FILE, encoding='utf-8') as f:
    notes = json.load(f)

added = 0
for qnum, text in NOTES.items():
    key = make_key(qnum)
    if key in notes:
        print(f"Q{qnum:02d}: already exists, skipping")
    else:
        notes[key] = text
        added += 1

with open(NOTES_FILE, "w", encoding='utf-8') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print(f"Done. Added {added} new notes.")
