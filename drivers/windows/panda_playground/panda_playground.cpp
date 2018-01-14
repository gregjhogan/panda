// panda_playground.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "pandaJ2534DLL Test\Loader4.h"
#include "ECUsim DLL\ECUsim.h"
#include <chrono>


int _tmain(int Argc, _TCHAR *Argv) {
	UNREFERENCED_PARAMETER(Argc);
	UNREFERENCED_PARAMETER(Argv);

	//ECUsim sim("", 500000);

	//if (LoadJ2534Dll("C:\\WINDOWS\\SysWOW64\\op20pt32.dll") != 0) {
	if (LoadJ2534Dll("..\\Debug_x86\\pandaJ2534_0404_32.dll") != 0) {
		auto err = GetLastError();
		return 1;
	}

	unsigned long did, cid, fid;
	PassThruOpen("", &did);
	PassThruConnect(did, ISO15765, CAN_29BIT_ID, 500000, &cid);

	PASSTHRU_MSG mask, pattern, flow;

	memcpy(mask.Data, "\xff\x00\x00\x00", 4);
	mask.DataSize = 4;
	mask.ProtocolID = ISO15765;
	mask.TxFlags = CAN_29BIT_ID;
	mask.ExtraDataIndex = 0;
	mask.RxStatus = 0;

	////////////////////////18//DA//F1//EF
	memcpy(pattern.Data, "\x18\x00\x00\x00", 4);
	pattern.DataSize = 4;
	pattern.ProtocolID = ISO15765;
	pattern.TxFlags = CAN_29BIT_ID;
	pattern.ExtraDataIndex = 0;
	pattern.RxStatus = 0;

	memcpy(flow.Data, "\x18\x00\x00\x00", 4);
	flow.DataSize = 4;
	flow.ProtocolID = ISO15765;
	flow.TxFlags = CAN_29BIT_ID;
	flow.ExtraDataIndex = 0;
	flow.RxStatus = 0;

	auto res = PassThruStartMsgFilter(cid, FLOW_CONTROL_FILTER, &mask, &pattern, &flow, &fid);
	if (res != STATUS_NOERROR)
		return 1;

	SCONFIG_LIST list;
	SCONFIG config;
	config.Parameter = LOOPBACK;
	config.Value = 0;
	list.ConfigPtr = &config;
	list.NumOfParams = 1;

	res = PassThruIoctl(cid, SET_CONFIG, &list, NULL);
	if (res != STATUS_NOERROR)
		return 1;

	char resMsg[128];
	for (auto cnt = 0; cnt < 3; cnt++)
	{
		PassThruIoctl(cid, CLEAR_TX_BUFFER, NULL, NULL);
		PassThruIoctl(cid, CLEAR_RX_BUFFER, NULL, NULL);

		PASSTHRU_MSG outmsg;
		memcpy(outmsg.Data, "\x18\xda\x10\xf1""\x02\x09\x02", 4 + 3);
		outmsg.DataSize = 4 + 3;
		outmsg.ProtocolID = ISO15765;
		outmsg.TxFlags = CAN_29BIT_ID;
		outmsg.ExtraDataIndex = 0;
		outmsg.RxStatus = 0;

		unsigned long msgoutcount = 1;

		printf("WRITE\n");
		res = PassThruWriteMsgs(cid, &outmsg, &msgoutcount, 0);
		resMsg[0] = '\0';
		PassThruGetLastError(resMsg);
		printf("result: %s\n", resMsg);

		PASSTHRU_MSG inmsg[128];
		unsigned long msgincount = 128;

		printf("READ\n");
		res = PassThruReadMsgs(cid, inmsg, &msgincount, 2000);
		resMsg[0] = '\0';
		PassThruGetLastError(resMsg);
		printf("result: %s\n", resMsg);
		printf("count: %d\n", msgincount);

		for (auto i = 0UL; i < msgincount; i++) {
			for (auto j = 0UL; j < inmsg[i].DataSize; j++) {
				printf("%02X", (unsigned char)inmsg[i].Data[j]);
			}
			printf("\nsize: %d\n", inmsg[i].DataSize);
		}

		Sleep(100);
	}

	PassThruDisconnect(cid);
	PassThruClose(did);

	return 0;
}
