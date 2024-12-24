use crate::OutlierInterval;

pub(crate) const SERIES: &[&[f64]] = &[
    &[
        84.57766308278907,
        1.4076132246566786,
        67.12849665338332,
        70.4844487925233,
        80.77724954996945,
        36.345769823163266,
        77.11633847411767,
        97.6707385111383,
        69.3742222608314,
        89.95850895798397,
        86.44058157728587,
        9.089376603932653,
        64.14679802150584,
        78.1988558948469,
        87.41730096783404,
        89.33905303940557,
        80.45457557497635,
        84.09581570682096,
        74.07672805009156,
        98.64264235031929,
        46.6792608776851,
        92.29501968947773,
        38.54286640761369,
        61.84150058492182,
        33.72509082208583,
        30.461520235489846,
        82.25437147764583,
        55.460871131051604,
        74.666725113154,
        91.09110664252076,
        10.332957487668072,
        14.733419891388966,
        97.01170658772136,
        58.85700337872668,
        38.28486264528148,
        45.00951206278911,
        6.252312717468245,
        88.38652975321506,
        36.54901608056296,
        20.148414943847627,
        45.48498515315023,
        11.21494003174095,
        33.608117643875765,
        26.645053110138118,
        25.248912843444614,
        3.065073643940419,
        5.649868075314779,
        71.52330571399206,
        80.05717348372173,
        36.78207573293128,
        90.54008075396864,
        51.76884221850604,
        7.33238987341589,
        60.31050738660299,
        87.26957253110905,
        57.573423834145146,
        28.87003449210337,
        71.90640431943804,
        91.37705676557044,
        79.79573745952638,
        9.50430920322387,
        16.493129644883233,
        38.58672755968235,
        7.324020299557454,
        8.446459747333446,
        52.296418079708154,
        83.83151622912901,
        68.409335443674,
        33.79669409447661,
        43.40681539521702,
        90.63342593718602,
        25.324961906544765,
        13.536102066816547,
        35.1712014748158,
        86.06630139886164,
        77.03924492918092,
        87.28716103807326,
        45.73617500015441,
        96.82095487331335,
        78.0557426209055,
        70.40067334743941,
        27.598214992309277,
        12.642298473421288,
        44.036234461260015,
        27.910078670147563,
        88.55216305112232,
        95.42332075259307,
        89.65355099544017,
        26.88767114285269,
        37.827870319742686,
        98.17833748346668,
        56.670079278676354,
        54.924724650653324,
        3.4247289084951227,
        56.70480828071873,
        16.842015970115433,
        7.288082345537128,
        33.88828558179156,
        72.20751031720476,
        98.75053255050128,
        84.57766308278907,
        1.4076132246566786,
        67.12849665338332,
        70.4844487925233,
        80.77724954996945,
        36.345769823163266,
        77.11633847411767,
        97.6707385111383,
        69.3742222608314,
        89.95850895798397,
        86.44058157728587,
        9.089376603932653,
        64.14679802150584,
        78.1988558948469,
        87.41730096783404,
        89.33905303940557,
        80.45457557497635,
        84.09581570682096,
        74.07672805009156,
        98.64264235031929,
        46.6792608776851,
        92.29501968947773,
        38.54286640761369,
        61.84150058492182,
        33.72509082208583,
        30.461520235489846,
        82.25437147764583,
        55.460871131051604,
        74.666725113154,
        91.09110664252076,
        10.332957487668072,
        14.733419891388966,
        97.01170658772136,
        58.85700337872668,
        38.28486264528148,
        45.00951206278911,
        6.252312717468245,
        88.38652975321506,
        36.54901608056296,
        20.148414943847627,
        45.48498515315023,
        11.21494003174095,
        33.608117643875765,
        26.645053110138118,
        25.248912843444614,
        3.065073643940419,
        5.649868075314779,
        71.52330571399206,
        80.05717348372173,
        36.78207573293128,
        90.54008075396864,
        51.76884221850604,
        7.33238987341589,
        60.31050738660299,
        87.26957253110905,
        57.573423834145146,
        28.87003449210337,
        71.90640431943804,
        91.37705676557044,
        79.79573745952638,
        9.50430920322387,
        16.493129644883233,
        38.58672755968235,
        7.324020299557454,
        8.446459747333446,
        52.296418079708154,
        83.83151622912901,
        68.409335443674,
        33.79669409447661,
        43.40681539521702,
        90.63342593718602,
        25.324961906544765,
        13.536102066816547,
        35.1712014748158,
        86.06630139886164,
        77.03924492918092,
        87.28716103807326,
        45.73617500015441,
        96.82095487331335,
        78.0557426209055,
        70.40067334743941,
        27.598214992309277,
        12.642298473421288,
        44.036234461260015,
        27.910078670147563,
        88.55216305112232,
        95.42332075259307,
        89.65355099544017,
        26.88767114285269,
        37.827870319742686,
        98.17833748346668,
        56.670079278676354,
        54.924724650653324,
        3.4247289084951227,
        56.70480828071873,
        16.842015970115433,
        7.288082345537128,
        33.88828558179156,
        72.20751031720476,
        98.75053255050128,
        84.57766308278907,
        1.4076132246566786,
        67.12849665338332,
        70.4844487925233,
        80.77724954996945,
        36.345769823163266,
        77.11633847411767,
        97.6707385111383,
        69.3742222608314,
        89.95850895798397,
        86.44058157728587,
        9.089376603932653,
        64.14679802150584,
        78.1988558948469,
        87.41730096783404,
        89.33905303940557,
        80.45457557497635,
        84.09581570682096,
        74.07672805009156,
        98.64264235031929,
        46.6792608776851,
        92.29501968947773,
        38.54286640761369,
        61.84150058492182,
        33.72509082208583,
        30.461520235489846,
        82.25437147764583,
        55.460871131051604,
        74.666725113154,
        91.09110664252076,
        10.332957487668072,
        14.733419891388966,
        97.01170658772136,
        58.85700337872668,
        38.28486264528148,
        45.00951206278911,
        6.252312717468245,
        88.38652975321506,
        36.54901608056296,
        20.148414943847627,
        45.48498515315023,
        11.21494003174095,
        33.608117643875765,
        26.645053110138118,
        25.248912843444614,
        3.065073643940419,
        5.649868075314779,
        71.52330571399206,
        80.05717348372173,
        36.78207573293128,
        90.54008075396864,
        51.76884221850604,
        7.33238987341589,
        60.31050738660299,
        87.26957253110905,
        57.573423834145146,
        28.87003449210337,
        71.90640431943804,
        91.37705676557044,
        79.79573745952638,
        9.50430920322387,
        16.493129644883233,
        38.58672755968235,
        7.324020299557454,
        8.446459747333446,
        52.296418079708154,
        83.83151622912901,
        68.409335443674,
        33.79669409447661,
        43.40681539521702,
        90.63342593718602,
        25.324961906544765,
        13.536102066816547,
        35.1712014748158,
        86.06630139886164,
        77.03924492918092,
        87.28716103807326,
        45.73617500015441,
        96.82095487331335,
        78.0557426209055,
        70.40067334743941,
        27.598214992309277,
        12.642298473421288,
        44.036234461260015,
        27.910078670147563,
        88.55216305112232,
        95.42332075259307,
        89.65355099544017,
        26.88767114285269,
    ],
    &[
        79.09740782667936,
        57.118709654178446,
        87.53323221207891,
        77.51851921751044,
        13.827991718617527,
        64.50072825165974,
        63.22243398177947,
        85.18147314148565,
        45.70579597640163,
        53.44987100797345,
        27.899715058639107,
        12.743519952211923,
        53.33112401220497,
        91.29194327065353,
        22.809628925227287,
        94.47045484736489,
        74.15721967907271,
        98.13118834152014,
        74.41875899164445,
        26.397645760066535,
        2.414560096619711,
        49.57740583172332,
        10.035388239632837,
        53.49355859989142,
        86.00767019324209,
        39.33742271773573,
        91.40075824214622,
        99.11698628952956,
        9.187627014050538,
        83.76161141023708,
        70.81510371685079,
        81.56976345760418,
        97.47520219853405,
        40.08027686572881,
        25.844190885831274,
        4.389526674383992,
        54.64641763550227,
        0.4231155756546645,
        23.583003444814608,
        44.1790735500464,
        95.7717981384677,
        65.55109191610991,
        28.84329684093696,
        72.87513411541494,
        24.68710897578923,
        53.550582494380365,
        93.57260308340692,
        93.28381457946564,
        4.672658941763164,
        64.16929073124258,
        65.56010285395746,
        48.53907226680969,
        26.21894593055176,
        36.09290585037477,
        36.078170088739256,
        37.779693331438956,
        58.14568587542899,
        15.548870881950538,
        53.106358130720174,
        45.56447065417781,
        63.94096989657414,
        23.7249007290824,
        35.23518765577438,
        83.3005631197085,
        81.76264009740768,
        70.6714593156112,
        96.19076939332984,
        97.15921554866922,
        48.2856089761567,
        44.63092020726545,
        68.47528994964497,
        12.803697483798238,
        94.28339595054318,
        96.96326449687236,
        82.8834517528233,
        75.80928718779066,
        52.93530904446329,
        26.17726356590573,
        7.871947467845675,
        4.6572490030445834,
        42.5272399131132,
        6.270700285524233,
        43.56190056272613,
        9.771900184030248,
        9.069149276015342,
        49.77604678691701,
        91.35722525049847,
        2.1072694958403027,
        80.26565470505192,
        84.83455261205923,
        75.58419504950665,
        9.577161214253316,
        30.8895668367555,
        58.00693947402493,
        2.948234829988605,
        74.7316977305968,
        34.15715618419488,
        4.160128651531814,
        30.049765912212088,
        99.02598540257061,
        79.09740782667936,
        57.118709654178446,
        87.53323221207891,
        77.51851921751044,
        13.827991718617527,
        64.50072825165974,
        63.22243398177947,
        85.18147314148565,
        45.70579597640163,
        53.44987100797345,
        27.899715058639107,
        12.743519952211923,
        53.33112401220497,
        91.29194327065353,
        22.809628925227287,
        94.47045484736489,
        74.15721967907271,
        98.13118834152014,
        74.41875899164445,
        26.397645760066535,
        2.414560096619711,
        49.57740583172332,
        10.035388239632837,
        53.49355859989142,
        86.00767019324209,
        39.33742271773573,
        91.40075824214622,
        99.11698628952956,
        9.187627014050538,
        83.76161141023708,
        70.81510371685079,
        81.56976345760418,
        97.47520219853405,
        40.08027686572881,
        25.844190885831274,
        4.389526674383992,
        54.64641763550227,
        0.4231155756546645,
        23.583003444814608,
        44.1790735500464,
        95.7717981384677,
        65.55109191610991,
        28.84329684093696,
        72.87513411541494,
        24.68710897578923,
        53.550582494380365,
        93.57260308340692,
        93.28381457946564,
        4.672658941763164,
        64.16929073124258,
        65.56010285395746,
        48.53907226680969,
        26.21894593055176,
        36.09290585037477,
        36.078170088739256,
        37.779693331438956,
        58.14568587542899,
        15.548870881950538,
        53.106358130720174,
        45.56447065417781,
        63.94096989657414,
        23.7249007290824,
        35.23518765577438,
        83.3005631197085,
        81.76264009740768,
        70.6714593156112,
        96.19076939332984,
        97.15921554866922,
        48.2856089761567,
        44.63092020726545,
        68.47528994964497,
        12.803697483798238,
        94.28339595054318,
        96.96326449687236,
        82.8834517528233,
        75.80928718779066,
        52.93530904446329,
        26.17726356590573,
        7.871947467845675,
        4.6572490030445834,
        42.5272399131132,
        6.270700285524233,
        43.56190056272613,
        9.771900184030248,
        9.069149276015342,
        49.77604678691701,
        91.35722525049847,
        2.1072694958403027,
        80.26565470505192,
        84.83455261205923,
        75.58419504950665,
        9.577161214253316,
        30.8895668367555,
        58.00693947402493,
        2.948234829988605,
        74.7316977305968,
        34.15715618419488,
        4.160128651531814,
        30.049765912212088,
        99.02598540257061,
        79.09740782667936,
        57.118709654178446,
        87.53323221207891,
        77.51851921751044,
        13.827991718617527,
        64.50072825165974,
        63.22243398177947,
        85.18147314148565,
        45.70579597640163,
        53.44987100797345,
        27.899715058639107,
        12.743519952211923,
        53.33112401220497,
        91.29194327065353,
        22.809628925227287,
        94.47045484736489,
        74.15721967907271,
        98.13118834152014,
        74.41875899164445,
        26.397645760066535,
        2.414560096619711,
        49.57740583172332,
        10.035388239632837,
        53.49355859989142,
        86.00767019324209,
        39.33742271773573,
        91.40075824214622,
        99.11698628952956,
        9.187627014050538,
        83.76161141023708,
        70.81510371685079,
        81.56976345760418,
        97.47520219853405,
        40.08027686572881,
        25.844190885831274,
        4.389526674383992,
        54.64641763550227,
        0.4231155756546645,
        23.583003444814608,
        44.1790735500464,
        95.7717981384677,
        65.55109191610991,
        28.84329684093696,
        72.87513411541494,
        24.68710897578923,
        53.550582494380365,
        93.57260308340692,
        93.28381457946564,
        4.672658941763164,
        64.16929073124258,
        65.56010285395746,
        48.53907226680969,
        26.21894593055176,
        36.09290585037477,
        36.078170088739256,
        37.779693331438956,
        58.14568587542899,
        15.548870881950538,
        53.106358130720174,
        45.56447065417781,
        63.94096989657414,
        23.7249007290824,
        35.23518765577438,
        83.3005631197085,
        81.76264009740768,
        70.6714593156112,
        96.19076939332984,
        97.15921554866922,
        48.2856089761567,
        44.63092020726545,
        68.47528994964497,
        12.803697483798238,
        94.28339595054318,
        96.96326449687236,
        82.8834517528233,
        75.80928718779066,
        52.93530904446329,
        26.17726356590573,
        7.871947467845675,
        4.6572490030445834,
        42.5272399131132,
        6.270700285524233,
        43.56190056272613,
        9.771900184030248,
        9.069149276015342,
        49.77604678691701,
        91.35722525049847,
        2.1072694958403027,
        80.26565470505192,
    ],
    &[
        61.19459989977207,
        7.901428710382974,
        11.84873090957308,
        42.62413268175682,
        26.64906044729647,
        27.57353110648564,
        8.37606302802374,
        93.05138279774955,
        72.86576339070214,
        29.506208300414173,
        91.42794110903219,
        83.31351824145901,
        71.79852167820488,
        83.89558439380946,
        66.90714108997138,
        11.105947284493434,
        19.244832097723318,
        44.230679984546775,
        20.099454514831507,
        6.350175387140533,
        41.077378863280444,
        12.529031628744857,
        64.48954251473495,
        18.461521448336214,
        0.3791039193137058,
        32.070249209047134,
        35.12996486662316,
        3.0111080155742043,
        59.781775219221814,
        62.29113348683264,
        3.544557813346594,
        91.15076657566577,
        76.46974490655845,
        56.76073710583629,
        30.690087196971948,
        44.8478302483067,
        94.97468245625866,
        45.33109617797058,
        98.14597947661596,
        89.06773828493068,
        333.78044245399343,
        738.5596094603311,
        84.4635985957161,
        25.814785400489313,
        66.61727654971747,
        67.05677822275702,
        11.341048598183345,
        61.52603827136127,
        59.706653296750446,
        52.06628442152088,
        51.71602489279004,
        63.456936337314396,
        93.3474276650534,
        4.257300795369279,
        2.629421774599061,
        43.21879609469734,
        35.376944510880605,
        82.14393735302066,
        84.89528082096123,
        9.159411323994181,
        7.896481178090808,
        51.18736626165597,
        69.8041575756628,
        8.721484612638575,
        60.18328959772108,
        37.490318144398,
        77.5656582542206,
        19.51006243954825,
        71.06052946932266,
        46.153580502016254,
        64.82704161760631,
        26.481968914124664,
        72.12535583427406,
        43.06214683770142,
        84.67999734877407,
        77.60644482162095,
        91.89538905253166,
        61.50970089262175,
        89.13343633034185,
        82.430632895014,
        70.92083108827212,
        63.290867421425425,
        35.03896362304457,
        16.330955293180317,
        28.626766484634537,
        21.927480056937434,
        18.69901859683747,
        29.801444509636553,
        90.21207715366646,
        2.9697260414931037,
        45.54728967831478,
        5.850530726058678,
        26.61406452048376,
        44.488516227309695,
        15.11049361088206,
        62.49921064345359,
        37.90144735664891,
        89.21126251105807,
        93.73709459644164,
        41.04276162237981,
        61.19459989977207,
        7.901428710382974,
        11.84873090957308,
        42.62413268175682,
        26.64906044729647,
        27.57353110648564,
        8.37606302802374,
        93.05138279774955,
        72.86576339070214,
        29.506208300414173,
        91.42794110903219,
        83.31351824145901,
        71.79852167820488,
        83.89558439380946,
        66.90714108997138,
        11.105947284493434,
        19.244832097723318,
        44.230679984546775,
        20.099454514831507,
        6.350175387140533,
        41.077378863280444,
        12.529031628744857,
        64.48954251473495,
        18.461521448336214,
        0.3791039193137058,
        32.070249209047134,
        35.12996486662316,
        3.0111080155742043,
        59.781775219221814,
        62.29113348683264,
        3.544557813346594,
        91.15076657566577,
        76.46974490655845,
        56.76073710583629,
        30.690087196971948,
        44.8478302483067,
        94.97468245625866,
        45.33109617797058,
        98.14597947661596,
        89.06773828493068,
        333.78044245399343,
        738.5596094603311,
        84.4635985957161,
        25.814785400489313,
        66.61727654971747,
        67.05677822275702,
        11.341048598183345,
        61.52603827136127,
        59.706653296750446,
        52.06628442152088,
        51.71602489279004,
        63.456936337314396,
        93.3474276650534,
        4.257300795369279,
        2.629421774599061,
        43.21879609469734,
        35.376944510880605,
        82.14393735302066,
        84.89528082096123,
        9.159411323994181,
        7.896481178090808,
        51.18736626165597,
        69.8041575756628,
        8.721484612638575,
        60.18328959772108,
        37.490318144398,
        77.5656582542206,
        19.51006243954825,
        71.06052946932266,
        46.153580502016254,
        64.82704161760631,
        26.481968914124664,
        72.12535583427406,
        43.06214683770142,
        84.67999734877407,
        77.60644482162095,
        91.89538905253166,
        61.50970089262175,
        89.13343633034185,
        82.430632895014,
        70.92083108827212,
        63.290867421425425,
        35.03896362304457,
        16.330955293180317,
        28.626766484634537,
        21.927480056937434,
        18.69901859683747,
        29.801444509636553,
        90.21207715366646,
        2.9697260414931037,
        45.54728967831478,
        5.850530726058678,
        26.61406452048376,
        44.488516227309695,
        15.11049361088206,
        62.49921064345359,
        37.90144735664891,
        89.21126251105807,
        93.73709459644164,
        41.04276162237981,
        61.19459989977207,
        7.901428710382974,
        11.84873090957308,
        42.62413268175682,
        26.64906044729647,
        27.57353110648564,
        8.37606302802374,
        93.05138279774955,
        72.86576339070214,
        29.506208300414173,
        91.42794110903219,
        83.31351824145901,
        71.79852167820488,
        83.89558439380946,
        66.90714108997138,
        11.105947284493434,
        19.244832097723318,
        44.230679984546775,
        20.099454514831507,
        6.350175387140533,
        41.077378863280444,
        12.529031628744857,
        64.48954251473495,
        18.461521448336214,
        0.3791039193137058,
        32.070249209047134,
        35.12996486662316,
        3.0111080155742043,
        59.781775219221814,
        62.29113348683264,
        3.544557813346594,
        91.15076657566577,
        76.46974490655845,
        56.76073710583629,
        30.690087196971948,
        44.8478302483067,
        94.97468245625866,
        45.33109617797058,
        98.14597947661596,
        89.06773828493068,
        333.78044245399343,
        738.5596094603311,
        84.4635985957161,
        25.814785400489313,
        66.61727654971747,
        67.05677822275702,
        11.341048598183345,
        61.52603827136127,
        59.706653296750446,
        52.06628442152088,
        51.71602489279004,
        63.456936337314396,
        93.3474276650534,
        4.257300795369279,
        2.629421774599061,
        43.21879609469734,
        35.376944510880605,
        82.14393735302066,
        84.89528082096123,
        9.159411323994181,
        7.896481178090808,
        51.18736626165597,
        69.8041575756628,
        8.721484612638575,
        60.18328959772108,
        37.490318144398,
        77.5656582542206,
        19.51006243954825,
        71.06052946932266,
        46.153580502016254,
        64.82704161760631,
        26.481968914124664,
        72.12535583427406,
        43.06214683770142,
        84.67999734877407,
        77.60644482162095,
        91.89538905253166,
        61.50970089262175,
        89.13343633034185,
        82.430632895014,
        70.92083108827212,
        63.290867421425425,
        35.03896362304457,
        16.330955293180317,
        28.626766484634537,
        21.927480056937434,
        18.69901859683747,
        29.801444509636553,
        90.21207715366646,
    ],
];

/// Convert an `OutlierIntervals` to a list of indices.
pub(crate) fn flatten_intervals(intervals: &[OutlierInterval]) -> Vec<usize> {
    intervals
        .iter()
        .flat_map(|x| {
            let mut out = vec![x.start];
            if let Some(end) = x.end {
                out.push(end);
            }
            out
        })
        .collect()
}
