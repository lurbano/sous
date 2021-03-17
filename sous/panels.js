function load_pid_panel(){
  pid_table = `<div id="pid_table">
    <table>
      <tr>
        <td colspan="6" class="table_caption"> PID Calculation </td>
      </tr>
      <tr>
        <th>Kp</th>
        <td id="Kp">
          <input type="text" id="Kp_in" class="K_param_input">
        </td>
        <th>e</th>
        <td id="T_error"></td>
        <td>=</td>
        <td id="p_term"></td>
      </tr>
      <tr>
        <th>Ki</th>
        <td id="Ki">
          <input type="text" id="Ki_in" class="K_param_input">
        </td>
        <th> e<sub>sum</sub> </th>
        <td id="T_err_sum"></td>
        <td>=</td>
        <td id="i_term"></td>
      </tr>
      <tr>
        <th>Kd</th>
        <td id="Kd">
          <input type="text" id="Kd_in" class="K_param_input">
        </td>
        <th>de/dt</th>
        <td id="dT_err"></td>
        <td>=</td>
        <td id="d_term"></td>
      </tr>
      <tr>
        <th colspan="5">PID Value</th>
        <td id="pidVal"></td>
      </tr>
    </table>
  </div>
  `
}
