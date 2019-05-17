import numpy as np

llf = np.array([-244.3852892951])

nobs = np.array([202])

k = np.array([5])

k_exog = np.array([1])

sigma = np.array([.81130812929037])

chi2 = np.array([73901.783883385])

df_model = np.array([3])

k_ar = np.array([1])

k_ma = np.array([2])

params = np.array([
    .91963917600489,
    -.89804855498306,
    1.3032353997768,
    .30230174935463,
    .65822088065264])

cov_params = np.array([
    .00622027554245,
    .00026933156699,
    -.00014478009121,
    -.00010527901395,
    .00006880952561,
    .00026933156699,
    .0023661521973,
    -.00263264462948,
    -.00241927046074,
    -.00069258998629,
    -.00014478009121,
    -.00263264462948,
    .003637275855,
    .0033625395431,
    .00072507981262,
    -.00010527901395,
    -.00241927046074,
    .0033625395431,
    .00312013997649,
    .00067166747844,
    .00006880952561,
    -.00069258998629,
    .00072507981262,
    .00067166747844,
    .00108477120916]).reshape(5, 5)

xb = np.array([
    .91963917016983,
    .91963917016983,
    .69261693954468,
    .76115423440933,
    .63710719347,
    .77478265762329,
    .61527073383331,
    .80501782894135,
    .62182641029358,
    .72158020734787,
    .66619211435318,
    .72980058193207,
    .64935982227325,
    .77660953998566,
    .6069877743721,
    .79818457365036,
    .60795724391937,
    .7583304643631,
    .68147450685501,
    .72765469551086,
    .69699174165726,
    .69102382659912,
    .67753201723099,
    .72617518901825,
    .69977235794067,
    .713603079319,
    .72478419542313,
    .68503832817078,
    .75677126646042,
    .79034942388535,
    .68609654903412,
    .83208250999451,
    .60605573654175,
    .80849212408066,
    .69862711429596,
    .80978256464005,
    .7383074760437,
    .78789436817169,
    .79390448331833,
    .79169547557831,
    .76283228397369,
    .87939429283142,
    .75783687829971,
    .85010063648224,
    .80657452344894,
    .86508285999298,
    .72368890047073,
    .86846202611923,
    .75351697206497,
    .74047154188156,
    .82022970914841,
    .73184186220169,
    .7623735666275,
    .74929028749466,
    .75702118873596,
    .79036456346512,
    .81429827213287,
    1.0007030963898,
    .70464313030243,
    1.2375881671906,
    .82733017206192,
    1.1780800819397,
    .83767229318619,
    1.3407131433487,
    .7835128903389,
    .99667322635651,
    .82677388191223,
    1.0330017805099,
    .78713357448578,
    .80603551864624,
    .91298097372055,
    .94862020015717,
    .83088356256485,
    1.1405943632126,
    .72683191299438,
    1.0197489261627,
    .88344657421112,
    1.1016070842743,
    1.0485582351685,
    1.1717364788055,
    .94894939661026,
    1.418029665947,
    1.2063212394714,
    1.3504880666733,
    1.4053744077682,
    1.5106836557388,
    .91192328929901,
    1.4546687602997,
    1.2100585699081,
    1.2459771633148,
    1.2914154529572,
    1.1733019351959,
    .80550068616867,
    .88859277963638,
    1.5257360935211,
    .49089628458023,
    .75268715620041,
    .92090040445328,
    .99410575628281,
    .87882828712463,
    1.1253950595856,
    .89082646369934,
    .9317963719368,
    .90858340263367,
    .82737028598785,
    1.0978132486343,
    .74325948953629,
    .98125350475311,
    1.0478370189667,
    .03625157848001,
    1.3422871828079,
    .51377469301224,
    1.3643686771393,
    .70055514574051,
    1.2559896707535,
    .71517109870911,
    1.1997950077057,
    .75360465049744,
    1.2862613201141,
    .79965251684189,
    1.2606881856918,
    1.018030166626,
    1.1752370595932,
    .69517260789871,
    1.597958445549,
    .65335071086884,
    1.4763361215591,
    1.2708671092987,
    1.0432199239731,
    .561203956604,
    1.2630445957184,
    .66821777820587,
    1.2384748458862,
    .70777904987335,
    1.2246036529541,
    .75373476743698,
    1.199233174324,
    .69312900304794,
    1.0659650564194,
    .80386221408844,
    .99243313074112,
    .78622406721115,
    1.1766475439072,
    .74267518520355,
    1.1679803133011,
    .85658311843872,
    .99335825443268,
    .79920876026154,
    1.1595865488052,
    .92043119668961,
    .98299539089203,
    .94316083192825,
    1.0661553144455,
    .6393609046936,
    .9456650018692,
    .91597771644592,
    .80332309007645,
    .65838772058487,
    1.1093089580536,
    .68860310316086,
    1.0485997200012,
    .89771980047226,
    .94581252336502,
    1.0480616092682,
    1.0014315843582,
    1.1307729482651,
    1.1770483255386,
    .89873492717743,
    1.2652103900909,
    .66434383392334,
    1.1431220769882,
    .44322970509529,
    .9269899725914,
    1.0786435604095,
    .82789659500122,
    1.0368362665176,
    1.0712716579437,
    .70438456535339,
    .88966482877731,
    1.009087562561,
    1.0887442827225,
    .88976800441742,
    1.2735350131989,
    1.0157470703125,
    .95522791147232,
    1.3003809452057,
    .73179203271866,
    2.4736785888672,
    -.25176140666008,
    1.9082181453705,
    .53501582145691,
    .7591078877449,
    1.0281100273132,
    1.6240043640137,
    .60095232725143,
    1.6211705207825,
    1.344465970993,
    1.124480009079,
    2.1775946617126,
    -.71973150968552,
    -.37754261493683,
    1.2329530715942,
    1.127131819725])

y = np.array([
    np.nan,
    29.899639129639,
    29.842617034912,
    30.111154556274,
    30.007108688354,
    30.314783096313,
    30.165269851685,
    30.555017471313,
    30.461826324463,
    30.531579971313,
    30.586193084717,
    30.709800720215,
    30.689361572266,
    30.986608505249,
    30.826986312866,
    31.178184509277,
    31.047958374023,
    31.238330841064,
    31.371475219727,
    31.477655410767,
    31.636991500854,
    31.641023635864,
    31.697532653809,
    31.846176147461,
    31.979772567749,
    32.093601226807,
    32.304782867432,
    32.335037231445,
    32.636772155762,
    33.070346832275,
    33.136096954346,
    33.682079315186,
    33.506057739258,
    33.908489227295,
    34.098628997803,
    34.509784698486,
    34.838306427002,
    35.187896728516,
    35.693904876709,
    36.091693878174,
    36.462833404541,
    37.179393768311,
    37.557834625244,
    38.150100708008,
    38.706577301025,
    39.365081787109,
    39.623691558838,
    40.268463134766,
    40.653518676758,
    40.840469360352,
    41.420227050781,
    41.631843566895,
    41.962375640869,
    42.249290466309,
    42.557022094727,
    42.990364074707,
    43.514297485352,
    44.700702667236,
    44.904644012451,
    46.837585449219,
    47.627330780029,
    49.278079986572,
    50.137672424316,
    52.340713500977,
    53.083511352539,
    53.996673583984,
    54.826774597168,
    55.933002471924,
    56.587131500244,
    56.906032562256,
    57.912979125977,
    58.848621368408,
    59.530883789063,
    61.140594482422,
    61.526832580566,
    62.619747161865,
    63.583446502686,
    65.001609802246,
    66.548561096191,
    68.27173614502,
    69.448951721191,
    72.018028259277,
    74.206321716309,
    76.550483703613,
    79.405372619629,
    82.410682678223,
    83.511924743652,
    86.154663085938,
    88.410057067871,
    90.345977783203,
    92.791412353516,
    94.573303222656,
    95.205505371094,
    95.888595581055,
    99.025733947754,
    98.590896606445,
    98.652687072754,
    99.720901489258,
    100.79410552979,
    101.67883300781,
    103.22539520264,
    104.19082641602,
    105.03179168701,
    106.00858306885,
    106.52736663818,
    108.09781646729,
    108.44326019287,
    109.48125457764,
    110.94783782959,
    108.73625183105,
    110.84228515625,
    110.71376800537,
    112.7643737793,
    113.40055084229,
    115.05599212646,
    115.71517181396,
    117.19979858398,
    117.95359802246,
    119.78626251221,
    120.69965362549,
    122.46068572998,
    124.1180267334,
    125.67523956299,
    126.09517669678,
    129.09796142578,
    129.55334472656,
    131.97633361816,
    134.67086791992,
    135.74320983887,
    135.66120910645,
    137.46304321289,
    137.86820983887,
    139.53848266602,
    140.10777282715,
    141.724609375,
    142.45373535156,
    143.99923706055,
    144.49313354492,
    145.56596374512,
    146.40386962891,
    147.29243469238,
    147.98622131348,
    149.57664489746,
    150.14266967773,
    151.66798400879,
    152.65658569336,
    153.59336853027,
    154.29920959473,
    155.85958862305,
    157.02043151855,
    157.98300170898,
    159.14315795898,
    160.46615600586,
    160.53935241699,
    161.34565734863,
    162.41598510742,
    162.80332946777,
    162.85838317871,
    164.30931091309,
    164.5885925293,
    165.74859619141,
    166.7977142334,
    167.64581298828,
    169.14807128906,
    170.30143737793,
    172.03076171875,
    173.87704467773,
    174.79872131348,
    176.86521911621,
    177.06433105469,
    178.54312133789,
    178.0432434082,
    178.62698364258,
    180.37864685059,
    180.82789611816,
    182.23683166504,
    183.67127990723,
    183.90438842773,
    184.58966064453,
    185.90908813477,
    187.38874816895,
    188.2897644043,
    190.37353515625,
    191.81575012207,
    192.75523376465,
    195.10038757324,
    195.43179321289,
    201.67367553711,
    199.14823913574,
    202.60821533203,
    203.23501586914,
    202.65910339355,
    204.60211181641,
    207.54400634766,
    207.93894958496,
    210.75416564941,
    213.83946228027,
    215.12147521973,
    220.78759765625,
    216.16928100586,
    211.79644775391,
    213.90396118164,
    215.59613037109])

resid = np.array([
    np.nan,
    -.74963909387589,
    -.49261617660522,
    -.74115377664566,
    -.46710711717606,
    -.76478433609009,
    -.41527000069618,
    -.71501767635345,
    -.65182709693909,
    -.61157959699631,
    -.6061926484108,
    -.66979920864105,
    -.47936165332794,
    -.76660931110382,
    -.44698792695999,
    -.73818320035934,
    -.56795823574066,
    -.54832947254181,
    -.62147504091263,
    -.53765416145325,
    -.68699151277542,
    -.6210241317749,
    -.57753163576126,
    -.56617534160614,
    -.59977388381958,
    -.51360231637955,
    -.65478450059891,
    -.45503878593445,
    -.35677161812782,
    -.62034744024277,
    -.2860988676548,
    -.78207945823669,
    -.40605875849724,
    -.50848907232285,
    -.39862787723541,
    -.40978488326073,
    -.43830442428589,
    -.28789436817169,
    -.39390674233437,
    -.3916939496994,
    -.16283383965492,
    -.37939432263374,
    -.25783684849739,
    -.25009834766388,
    -.20657606422901,
    -.46508130431175,
    -.22368888556957,
    -.36846202611923,
    -.55352002382278,
    -.24047155678272,
    -.52022665739059,
    -.43184259533882,
    -.46237435936928,
    -.44929105043411,
    -.35701966285706,
    -.29036456346512,
    .1857016980648,
    -.50070303678513,
    .69535458087921,
    -.03758737072349,
    .47266906499863,
    .02192067168653,
    .86232846975327,
    -.04071394726634,
    -.08351214230061,
    .0033267585095,
    .07322765141726,
    -.13300403952599,
    -.48713436722755,
    .09396601468325,
    -.01297946088016,
    -.14862097799778,
    .4691156744957,
    -.34059509634972,
    .073167309165,
    .08025334775448,
    .31655418872833,
    .49839133024216,
    .55144023895264,
    .22826506197453,
    1.1510490179062,
    .9819718003273,
    .9936757683754,
    1.4495149850845,
    1.4946271181107,
    .18931329250336,
    1.1880751848221,
    1.0453312397003,
    .68994289636612,
    1.1540243625641,
    .60858601331711,
    -.17330189049244,
    -.20550219714642,
    1.611407160759,
    -.92573761940002,
    -.69089323282242,
    .14731439948082,
    .07909959554672,
    .00589422974735,
    .42116710543633,
    .07460948079824,
    -.09083105623722,
    .06820363551378,
    -.30858492851257,
    .47263273596764,
    -.39781630039215,
    .05674355849624,
    .41874802112579,
    -2.2478415966034,
    .76375144720078,
    -.64229023456573,
    .68622988462448,
    -.06437320262194,
    .39945095777512,
    -.0559926815331,
    .28482890129089,
    .00020190737268,
    .54639840126038,
    .11374024301767,
    .50034290552139,
    .63931334018707,
    .38197138905525,
    -.27523550391197,
    1.404825925827,
    -.1979645639658,
    .94665539264679,
    1.4236577749252,
    .02913599461317,
    -.643210709095,
    .53878688812256,
    -.26304465532303,
    .43178829550743,
    -.13848400115967,
    .39222705364227,
    -.02460673451424,
    .34627133607864,
    -.19923311471939,
    .00686796056107,
    .03404098749161,
    -.10386525094509,
    -.09243924915791,
    .41377285122871,
    -.17664749920368,
    .35733091831207,
    .13202276825905,
    -.05658006668091,
    -.09336434304714,
    .40078815817833,
    .24042254686356,
    -.02043732441962,
    .217001542449,
    .25683608651161,
    -.56615537405014,
    -.13936093449593,
    .15434110164642,
    -.41597774624825,
    -.60332614183426,
    .34161224961281,
    -.40931203961372,
    .11139994114637,
    .15139718353748,
    -.09771674126387,
    .45419663190842,
    .15193535387516,
    .5985592007637,
    .66923010349274,
    .02294866926968,
    .80127727985382,
    -.46522265672684,
    .33565619587898,
    -.94310986995697,
    -.34323886036873,
    .67301613092422,
    -.37864658236504,
    .37210035324097,
    .3631728887558,
    -.47128081321716,
    -.20438456535339,
    .3103321492672,
    .3909215927124,
    .01124659087509,
    .81024420261383,
    .42646199464798,
    -.01574708521366,
    1.044772028923,
    -.40038701891899,
    3.768208026886,
    -2.273681640625,
    1.5517644882202,
    .09178187698126,
    -1.3350188732147,
    .91490334272385,
    1.317883014679,
    -.20600511133671,
    1.1940457820892,
    1.7408289909363,
    .15753293037415,
    3.4885265827179,
    -3.8985877037048,
    -3.9952800273895,
    .87455189228058,
    .56503582000732,
    .78886848688126])

yr = np.array([
    np.nan,
    -.74963909387589,
    -.49261617660522,
    -.74115377664566,
    -.46710711717606,
    -.76478433609009,
    -.41527000069618,
    -.71501767635345,
    -.65182709693909,
    -.61157959699631,
    -.6061926484108,
    -.66979920864105,
    -.47936165332794,
    -.76660931110382,
    -.44698792695999,
    -.73818320035934,
    -.56795823574066,
    -.54832947254181,
    -.62147504091263,
    -.53765416145325,
    -.68699151277542,
    -.6210241317749,
    -.57753163576126,
    -.56617534160614,
    -.59977388381958,
    -.51360231637955,
    -.65478450059891,
    -.45503878593445,
    -.35677161812782,
    -.62034744024277,
    -.2860988676548,
    -.78207945823669,
    -.40605875849724,
    -.50848907232285,
    -.39862787723541,
    -.40978488326073,
    -.43830442428589,
    -.28789436817169,
    -.39390674233437,
    -.3916939496994,
    -.16283383965492,
    -.37939432263374,
    -.25783684849739,
    -.25009834766388,
    -.20657606422901,
    -.46508130431175,
    -.22368888556957,
    -.36846202611923,
    -.55352002382278,
    -.24047155678272,
    -.52022665739059,
    -.43184259533882,
    -.46237435936928,
    -.44929105043411,
    -.35701966285706,
    -.29036456346512,
    .1857016980648,
    -.50070303678513,
    .69535458087921,
    -.03758737072349,
    .47266906499863,
    .02192067168653,
    .86232846975327,
    -.04071394726634,
    -.08351214230061,
    .0033267585095,
    .07322765141726,
    -.13300403952599,
    -.48713436722755,
    .09396601468325,
    -.01297946088016,
    -.14862097799778,
    .4691156744957,
    -.34059509634972,
    .073167309165,
    .08025334775448,
    .31655418872833,
    .49839133024216,
    .55144023895264,
    .22826506197453,
    1.1510490179062,
    .9819718003273,
    .9936757683754,
    1.4495149850845,
    1.4946271181107,
    .18931329250336,
    1.1880751848221,
    1.0453312397003,
    .68994289636612,
    1.1540243625641,
    .60858601331711,
    -.17330189049244,
    -.20550219714642,
    1.611407160759,
    -.92573761940002,
    -.69089323282242,
    .14731439948082,
    .07909959554672,
    .00589422974735,
    .42116710543633,
    .07460948079824,
    -.09083105623722,
    .06820363551378,
    -.30858492851257,
    .47263273596764,
    -.39781630039215,
    .05674355849624,
    .41874802112579,
    -2.2478415966034,
    .76375144720078,
    -.64229023456573,
    .68622988462448,
    -.06437320262194,
    .39945095777512,
    -.0559926815331,
    .28482890129089,
    .00020190737268,
    .54639840126038,
    .11374024301767,
    .50034290552139,
    .63931334018707,
    .38197138905525,
    -.27523550391197,
    1.404825925827,
    -.1979645639658,
    .94665539264679,
    1.4236577749252,
    .02913599461317,
    -.643210709095,
    .53878688812256,
    -.26304465532303,
    .43178829550743,
    -.13848400115967,
    .39222705364227,
    -.02460673451424,
    .34627133607864,
    -.19923311471939,
    .00686796056107,
    .03404098749161,
    -.10386525094509,
    -.09243924915791,
    .41377285122871,
    -.17664749920368,
    .35733091831207,
    .13202276825905,
    -.05658006668091,
    -.09336434304714,
    .40078815817833,
    .24042254686356,
    -.02043732441962,
    .217001542449,
    .25683608651161,
    -.56615537405014,
    -.13936093449593,
    .15434110164642,
    -.41597774624825,
    -.60332614183426,
    .34161224961281,
    -.40931203961372,
    .11139994114637,
    .15139718353748,
    -.09771674126387,
    .45419663190842,
    .15193535387516,
    .5985592007637,
    .66923010349274,
    .02294866926968,
    .80127727985382,
    -.46522265672684,
    .33565619587898,
    -.94310986995697,
    -.34323886036873,
    .67301613092422,
    -.37864658236504,
    .37210035324097,
    .3631728887558,
    -.47128081321716,
    -.20438456535339,
    .3103321492672,
    .3909215927124,
    .01124659087509,
    .81024420261383,
    .42646199464798,
    -.01574708521366,
    1.044772028923,
    -.40038701891899,
    3.768208026886,
    -2.273681640625,
    1.5517644882202,
    .09178187698126,
    -1.3350188732147,
    .91490334272385,
    1.317883014679,
    -.20600511133671,
    1.1940457820892,
    1.7408289909363,
    .15753293037415,
    3.4885265827179,
    -3.8985877037048,
    -3.9952800273895,
    .87455189228058,
    .56503582000732,
    .78886848688126])

mse = np.array([
    1.8363103866577,
    .82643759250641,
    .69298559427261,
    .67553198337555,
    .67162227630615,
    .67045229673386,
    .66999220848083,
    .66973727941513,
    .66954612731934,
    .66937738656998,
    .66921871900558,
    .66906636953354,
    .66891890764236,
    .66877597570419,
    .66863715648651,
    .66850233078003,
    .66837131977081,
    .66824388504028,
    .6681199669838,
    .66799944639206,
    .6678820848465,
    .66776782274246,
    .66765648126602,
    .66754806041718,
    .66744232177734,
    .66733926534653,
    .66723877191544,
    .66714072227478,
    .66704499721527,
    .66695153713226,
    .66686034202576,
    .66677123308182,
    .66668421030045,
    .66659909486771,
    .66651594638824,
    .66643464565277,
    .66635513305664,
    .66627734899521,
    .66620123386383,
    .66612672805786,
    .6660538315773,
    .66598242521286,
    .66591250896454,
    .66584402322769,
    .66577690839767,
    .66571110486984,
    .66564667224884,
    .66558349132538,
    .66552156209946,
    .66546076536179,
    .66540116071701,
    .66534268856049,
    .66528534889221,
    .6652290225029,
    .66517376899719,
    .6651194691658,
    .66506624221802,
    .6650139093399,
    .66496247053146,
    .66491198539734,
    .66486239433289,
    .66481363773346,
    .6647657752037,
    .66471868753433,
    .66467237472534,
    .66462683677673,
    .66458207368851,
    .66453808546066,
    .66449475288391,
    .6644521355629,
    .66441023349762,
    .66436898708344,
    .66432839632034,
    .66428846120834,
    .66424912214279,
    .66421037912369,
    .66417229175568,
    .66413474082947,
    .66409778594971,
    .66406136751175,
    .66402548551559,
    .66399013996124,
    .66395533084869,
    .6639209985733,
    .66388720273972,
    .66385388374329,
    .66382104158401,
    .66378861665726,
    .6637567281723,
    .66372525691986,
    .66369420289993,
    .66366362571716,
    .66363340616226,
    .66360366344452,
    .66357427835464,
    .66354531049728,
    .66351670026779,
    .66348850727081,
    .6634606719017,
    .66343319416046,
    .66340607404709,
    .66337931156158,
    .66335290670395,
    .66332685947418,
    .66330111026764,
    .66327565908432,
    .66325056552887,
    .66322582960129,
    .66320133209229,
    .66317713260651,
    .6631532907486,
    .66312968730927,
    .66310638189316,
    .66308337450027,
    .66306066513062,
    .66303819417953,
    .66301596164703,
    .66299402713776,
    .6629723906517,
    .66295093297958,
    .66292977333069,
    .66290885210037,
    .66288816928864,
    .66286766529083,
    .66284745931625,
    .66282749176025,
    .66280770301819,
    .6627881526947,
    .66276878118515,
    .66274970769882,
    .66273081302643,
    .66271209716797,
    .66269356012344,
    .6626752614975,
    .66265720129013,
    .66263926029205,
    .66262155771255,
    .66260403394699,
    .66258668899536,
    .66256952285767,
    .66255259513855,
    .66253578662872,
    .66251915693283,
    .66250270605087,
    .6624863743782,
    .66247028112411,
    .66245430707932,
    .66243851184845,
    .66242289543152,
    .66240739822388,
    .66239207983017,
    .6623769402504,
    .66236186027527,
    .66234701871872,
    .66233229637146,
    .66231769323349,
    .66230326890945,
    .66228896379471,
    .66227477788925,
    .66226077079773,
    .6622468829155,
    .66223311424255,
    .6622194647789,
    .66220593452454,
    .66219258308411,
    .66217935085297,
    .66216617822647,
    .66215318441391,
    .66214030981064,
    .66212749481201,
    .66211485862732,
    .66210234165192,
    .66208988428116,
    .66207760572433,
    .66206538677216,
    .66205328702927,
    .66204130649567,
    .66202944517136,
    .66201764345169,
    .66200596094131,
    .66199439764023,
    .66198295354843,
    .66197156906128,
    .66196030378342,
    .66194915771484,
    .66193807125092,
    .66192710399628,
    .66191619634628,
    .66190540790558,
    .66189467906952,
    .66188406944275,
    .66187357902527,
    .66186314821243,
    .66185277700424,
    .66184252500534,
    .66183233261108,
    .66182225942612,
    .66181224584579,
    .66180229187012,
    .66179245710373,
    .66178268194199,
    .66177302598953,
    .66176337003708])

stdp = np.array([
    .91963917016983,
    .91963917016983,
    .69261693954468,
    .76115423440933,
    .63710719347,
    .77478265762329,
    .61527073383331,
    .80501782894135,
    .62182641029358,
    .72158020734787,
    .66619211435318,
    .72980058193207,
    .64935982227325,
    .77660953998566,
    .6069877743721,
    .79818457365036,
    .60795724391937,
    .7583304643631,
    .68147450685501,
    .72765469551086,
    .69699174165726,
    .69102382659912,
    .67753201723099,
    .72617518901825,
    .69977235794067,
    .713603079319,
    .72478419542313,
    .68503832817078,
    .75677126646042,
    .79034942388535,
    .68609654903412,
    .83208250999451,
    .60605573654175,
    .80849212408066,
    .69862711429596,
    .80978256464005,
    .7383074760437,
    .78789436817169,
    .79390448331833,
    .79169547557831,
    .76283228397369,
    .87939429283142,
    .75783687829971,
    .85010063648224,
    .80657452344894,
    .86508285999298,
    .72368890047073,
    .86846202611923,
    .75351697206497,
    .74047154188156,
    .82022970914841,
    .73184186220169,
    .7623735666275,
    .74929028749466,
    .75702118873596,
    .79036456346512,
    .81429827213287,
    1.0007030963898,
    .70464313030243,
    1.2375881671906,
    .82733017206192,
    1.1780800819397,
    .83767229318619,
    1.3407131433487,
    .7835128903389,
    .99667322635651,
    .82677388191223,
    1.0330017805099,
    .78713357448578,
    .80603551864624,
    .91298097372055,
    .94862020015717,
    .83088356256485,
    1.1405943632126,
    .72683191299438,
    1.0197489261627,
    .88344657421112,
    1.1016070842743,
    1.0485582351685,
    1.1717364788055,
    .94894939661026,
    1.418029665947,
    1.2063212394714,
    1.3504880666733,
    1.4053744077682,
    1.5106836557388,
    .91192328929901,
    1.4546687602997,
    1.2100585699081,
    1.2459771633148,
    1.2914154529572,
    1.1733019351959,
    .80550068616867,
    .88859277963638,
    1.5257360935211,
    .49089628458023,
    .75268715620041,
    .92090040445328,
    .99410575628281,
    .87882828712463,
    1.1253950595856,
    .89082646369934,
    .9317963719368,
    .90858340263367,
    .82737028598785,
    1.0978132486343,
    .74325948953629,
    .98125350475311,
    1.0478370189667,
    .03625157848001,
    1.3422871828079,
    .51377469301224,
    1.3643686771393,
    .70055514574051,
    1.2559896707535,
    .71517109870911,
    1.1997950077057,
    .75360465049744,
    1.2862613201141,
    .79965251684189,
    1.2606881856918,
    1.018030166626,
    1.1752370595932,
    .69517260789871,
    1.597958445549,
    .65335071086884,
    1.4763361215591,
    1.2708671092987,
    1.0432199239731,
    .561203956604,
    1.2630445957184,
    .66821777820587,
    1.2384748458862,
    .70777904987335,
    1.2246036529541,
    .75373476743698,
    1.199233174324,
    .69312900304794,
    1.0659650564194,
    .80386221408844,
    .99243313074112,
    .78622406721115,
    1.1766475439072,
    .74267518520355,
    1.1679803133011,
    .85658311843872,
    .99335825443268,
    .79920876026154,
    1.1595865488052,
    .92043119668961,
    .98299539089203,
    .94316083192825,
    1.0661553144455,
    .6393609046936,
    .9456650018692,
    .91597771644592,
    .80332309007645,
    .65838772058487,
    1.1093089580536,
    .68860310316086,
    1.0485997200012,
    .89771980047226,
    .94581252336502,
    1.0480616092682,
    1.0014315843582,
    1.1307729482651,
    1.1770483255386,
    .89873492717743,
    1.2652103900909,
    .66434383392334,
    1.1431220769882,
    .44322970509529,
    .9269899725914,
    1.0786435604095,
    .82789659500122,
    1.0368362665176,
    1.0712716579437,
    .70438456535339,
    .88966482877731,
    1.009087562561,
    1.0887442827225,
    .88976800441742,
    1.2735350131989,
    1.0157470703125,
    .95522791147232,
    1.3003809452057,
    .73179203271866,
    2.4736785888672,
    -.25176140666008,
    1.9082181453705,
    .53501582145691,
    .7591078877449,
    1.0281100273132,
    1.6240043640137,
    .60095232725143,
    1.6211705207825,
    1.344465970993,
    1.124480009079,
    2.1775946617126,
    -.71973150968552,
    -.37754261493683,
    1.2329530715942,
    1.127131819725])

icstats = np.array([
    202,
    np.nan,
    -244.3852892951,
    5,
    498.7705785902,
    515.31191707721])


class Bunch(dict):
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__ = self


results = Bunch(
    llf=llf,
    nobs=nobs,
    k=k,
    k_exog=k_exog,
    sigma=sigma,
    chi2=chi2,
    df_model=df_model,
    k_ar=k_ar,
    k_ma=k_ma,
    params=params,
    cov_params=cov_params,
    xb=xb,
    y=y,
    resid=resid,
    yr=yr,
    mse=mse,
    stdp=stdp,
    icstats=icstats
)
