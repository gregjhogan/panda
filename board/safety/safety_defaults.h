int default_rx_hook(CAN_FIFOMailBox_TypeDef *to_push) {
  UNUSED(to_push);
  return true;
}

// *** no output safety mode ***

static void nooutput_init(int16_t param) {
  UNUSED(param);
  controls_allowed = false;
  relay_malfunction_reset();
}

static int nooutput_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {
  UNUSED(to_send);
  return false;
}

static int nooutput_tx_lin_hook(int lin_num, uint8_t *data, int len) {
  UNUSED(lin_num);
  UNUSED(data);
  UNUSED(len);
  return false;
}

unsigned int fwd_cnt = 0;
static int default_fwd_hook(int bus_num, CAN_FIFOMailBox_TypeDef *to_fwd) {
  // UNUSED(bus_num);
  // UNUSED(to_fwd);
  // return -1;
  int bus_fwd = -1;
  int addr = GET_ADDR(to_fwd);
  // forward cam to ccan and viceversa, except lkas cmd
  if (!relay_malfunction) {
    //if (bus_num == 0) {
    if ((bus_num == 0) && (addr != 0x222) && (addr != 0x223) && (addr != 0x224) && (addr != 0x225)) {
      bus_fwd = 2;
    }
    // else if ((bus_num == 0) && (addr == 0x225)) {// && GET_BYTE(to_fwd, 0) == 0 && GET_BYTE(to_fwd, 1) == 0) {
    //   // to_fwd->RDLR = (to_fwd->RDLR & 0xFF00FFFF) | (((int)(fwd_cnt++ / 3) % 4) << 16);
    //   bus_fwd = 2;
    // }
    //if ((bus_num == 2) && (addr != 832) && (addr != 1157)) {
    if (bus_num == 2) {
      bus_fwd = 0;
    }
  }
  return bus_fwd;
}

const safety_hooks nooutput_hooks = {
  .init = nooutput_init,
  .rx = default_rx_hook,
  .tx = nooutput_tx_hook,
  .tx_lin = nooutput_tx_lin_hook,
  .fwd = default_fwd_hook,
};

// *** all output safety mode ***

static void alloutput_init(int16_t param) {
  UNUSED(param);
  controls_allowed = true;
  relay_malfunction_reset();
}

static int alloutput_tx_hook(CAN_FIFOMailBox_TypeDef *to_send) {
  UNUSED(to_send);
  return true;
}

static int alloutput_tx_lin_hook(int lin_num, uint8_t *data, int len) {
  UNUSED(lin_num);
  UNUSED(data);
  UNUSED(len);
  return true;
}

const safety_hooks alloutput_hooks = {
  .init = alloutput_init,
  .rx = default_rx_hook,
  .tx = alloutput_tx_hook,
  .tx_lin = alloutput_tx_lin_hook,
  .fwd = default_fwd_hook,
};
