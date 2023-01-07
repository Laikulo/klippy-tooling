# Wrapper around C helper code
#
# Copyright (C) 2016-2021  Kevin O'Connor <kevin@koconnor.net>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import os, logging
import cffi

DEST_LIB = "c_helper.so"

defs_stepcompress = """
    struct pull_history_steps {
        uint64_t first_clock, last_clock;
        int64_t start_position;
        int step_count, interval, add;
    };

    struct stepcompress *stepcompress_alloc(uint32_t oid);
    void stepcompress_fill(struct stepcompress *sc, uint32_t max_error
        , int32_t queue_step_msgtag, int32_t set_next_step_dir_msgtag);
    void stepcompress_set_invert_sdir(struct stepcompress *sc
        , uint32_t invert_sdir);
    void stepcompress_free(struct stepcompress *sc);
    int stepcompress_reset(struct stepcompress *sc, uint64_t last_step_clock);
    int stepcompress_set_last_position(struct stepcompress *sc
        , uint64_t clock, int64_t last_position);
    int64_t stepcompress_find_past_position(struct stepcompress *sc
        , uint64_t clock);
    int stepcompress_queue_msg(struct stepcompress *sc
        , uint32_t *data, int len);
    int stepcompress_extract_old(struct stepcompress *sc
        , struct pull_history_steps *p, int max
        , uint64_t start_clock, uint64_t end_clock);

    struct steppersync *steppersync_alloc(struct serialqueue *sq
        , struct stepcompress **sc_list, int sc_num, int move_num);
    void steppersync_free(struct steppersync *ss);
    void steppersync_set_time(struct steppersync *ss
        , double time_offset, double mcu_freq);
    int steppersync_flush(struct steppersync *ss, uint64_t move_clock);
"""

defs_itersolve = """
    int32_t itersolve_generate_steps(struct stepper_kinematics *sk
        , double flush_time);
    double itersolve_check_active(struct stepper_kinematics *sk
        , double flush_time);
    int32_t itersolve_is_active_axis(struct stepper_kinematics *sk, char axis);
    void itersolve_set_trapq(struct stepper_kinematics *sk, struct trapq *tq);
    void itersolve_set_stepcompress(struct stepper_kinematics *sk
        , struct stepcompress *sc, double step_dist);
    double itersolve_calc_position_from_coord(struct stepper_kinematics *sk
        , double x, double y, double z);
    void itersolve_set_position(struct stepper_kinematics *sk
        , double x, double y, double z);
    double itersolve_get_commanded_pos(struct stepper_kinematics *sk);
"""

defs_trapq = """
    struct pull_move {
        double print_time, move_t;
        double start_v, accel;
        double start_x, start_y, start_z;
        double x_r, y_r, z_r;
    };

    void trapq_append(struct trapq *tq, double print_time
        , double accel_t, double cruise_t, double decel_t
        , double start_pos_x, double start_pos_y, double start_pos_z
        , double axes_r_x, double axes_r_y, double axes_r_z
        , double start_v, double cruise_v, double accel);
    struct trapq *trapq_alloc(void);
    void trapq_free(struct trapq *tq);
    void trapq_finalize_moves(struct trapq *tq, double print_time);
    void trapq_set_position(struct trapq *tq, double print_time
        , double pos_x, double pos_y, double pos_z);
    int trapq_extract_old(struct trapq *tq, struct pull_move *p, int max
        , double start_time, double end_time);
"""

defs_kin_cartesian = """
    struct stepper_kinematics *cartesian_stepper_alloc(char axis);
    struct stepper_kinematics *cartesian_reverse_stepper_alloc(char axis);
"""

defs_kin_corexy = """
    struct stepper_kinematics *corexy_stepper_alloc(char type);
"""

defs_kin_corexz = """
    struct stepper_kinematics *corexz_stepper_alloc(char type);
"""

defs_kin_delta = """
    struct stepper_kinematics *delta_stepper_alloc(double arm2
        , double tower_x, double tower_y);
"""

defs_kin_deltesian = """
    struct stepper_kinematics *deltesian_stepper_alloc(double arm2
        , double arm_x);
"""

defs_kin_polar = """
    struct stepper_kinematics *polar_stepper_alloc(char type);
"""

defs_kin_rotary_delta = """
    struct stepper_kinematics *rotary_delta_stepper_alloc(
        double shoulder_radius, double shoulder_height
        , double angle, double upper_arm, double lower_arm);
"""

defs_kin_winch = """
    struct stepper_kinematics *winch_stepper_alloc(double anchor_x
        , double anchor_y, double anchor_z);
"""

defs_kin_extruder = """
    struct stepper_kinematics *extruder_stepper_alloc(void);
    void extruder_set_pressure_advance(struct stepper_kinematics *sk
        , double pressure_advance, double smooth_time);
"""

defs_kin_shaper = """
    double input_shaper_get_step_generation_window(int n, double a[]
        , double t[]);
    int input_shaper_set_shaper_params(struct stepper_kinematics *sk, char axis
        , int n, double a[], double t[]);
    int input_shaper_set_sk(struct stepper_kinematics *sk
        , struct stepper_kinematics *orig_sk);
    struct stepper_kinematics * input_shaper_alloc(void);
"""

defs_serialqueue = """
    #define MESSAGE_MAX 64
    struct pull_queue_message {
        uint8_t msg[MESSAGE_MAX];
        int len;
        double sent_time, receive_time;
        uint64_t notify_id;
    };

    struct serialqueue *serialqueue_alloc(int serial_fd, char serial_fd_type
        , int client_id);
    void serialqueue_exit(struct serialqueue *sq);
    void serialqueue_free(struct serialqueue *sq);
    struct command_queue *serialqueue_alloc_commandqueue(void);
    void serialqueue_free_commandqueue(struct command_queue *cq);
    void serialqueue_send(struct serialqueue *sq, struct command_queue *cq
        , uint8_t *msg, int len, uint64_t min_clock, uint64_t req_clock
        , uint64_t notify_id);
    void serialqueue_pull(struct serialqueue *sq
        , struct pull_queue_message *pqm);
    void serialqueue_set_wire_frequency(struct serialqueue *sq
        , double frequency);
    void serialqueue_set_receive_window(struct serialqueue *sq
        , int receive_window);
    void serialqueue_set_clock_est(struct serialqueue *sq, double est_freq
        , double conv_time, uint64_t conv_clock, uint64_t last_clock);
    void serialqueue_get_stats(struct serialqueue *sq, char *buf, int len);
    int serialqueue_extract_old(struct serialqueue *sq, int sentq
        , struct pull_queue_message *q, int max);
"""

defs_trdispatch = """
    void trdispatch_start(struct trdispatch *td, uint32_t dispatch_reason);
    void trdispatch_stop(struct trdispatch *td);
    struct trdispatch *trdispatch_alloc(void);
    struct trdispatch_mcu *trdispatch_mcu_alloc(struct trdispatch *td
        , struct serialqueue *sq, struct command_queue *cq, uint32_t trsync_oid
        , uint32_t set_timeout_msgtag, uint32_t trigger_msgtag
        , uint32_t state_msgtag);
    void trdispatch_mcu_setup(struct trdispatch_mcu *tdm
        , uint64_t last_status_clock, uint64_t expire_clock
        , uint64_t expire_ticks, uint64_t min_extend_ticks);
"""

defs_pyhelper = """
    void set_python_logging_callback(void (*func)(const char *));
    double get_monotonic(void);
"""

defs_std = """
    void free(void*);
"""

defs_all = [
    defs_pyhelper, defs_serialqueue, defs_std, defs_stepcompress,
    defs_itersolve, defs_trapq, defs_trdispatch,
    defs_kin_cartesian, defs_kin_corexy, defs_kin_corexz, defs_kin_delta,
    defs_kin_deltesian, defs_kin_polar, defs_kin_rotary_delta, defs_kin_winch,
    defs_kin_extruder, defs_kin_shaper,
]

FFI_main = None
FFI_lib = None
pyhelper_logging_callback = None

# Hepler invoked from C errorf() code to log errors
def logging_callback(msg):
    logging.error(FFI_main.string(msg))

# Return the Foreign Function Interface api to the caller
def get_ffi():
    global FFI_main, FFI_lib, pyhelper_logging_callback
    if FFI_lib is None:
        FFI_main = cffi.FFI()
        for d in defs_all:
            FFI_main.cdef(d)
        FFI_lib = FFI_main.dlopen(os.path.join(os.path.dirname(__file__),"c_helper.so"))
        # Setup error logging
        pyhelper_logging_callback = FFI_main.callback("void func(const char *)",
                                                      logging_callback)
        FFI_lib.set_python_logging_callback(pyhelper_logging_callback)
    return FFI_main, FFI_lib


######################################################################
# hub-ctrl hub power controller
######################################################################

# Sudo removed, as we assume udev rules grand this user access to /dev/bus/usb/ as needed
HC_CMD = "%s/hub-ctrl -h 0 -P 2 -p %d"

def run_hub_ctrl(enable_power):
    hubdir=os.path.dirname(__file__)
    os.system(HC_CMD % (hubdir, enable_power))


if __name__ == '__main__':
    get_ffi()
