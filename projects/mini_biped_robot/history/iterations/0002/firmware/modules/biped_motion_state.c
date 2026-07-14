/* Generated module: biped_motion_state — behavior: state_machine
 * States: DISARMED, CALIBRATE, STAND, WALK_FORWARD, TURN_LEFT, TURN_RIGHT, STOP, FALLEN, FAULT
 * Transitions: 16
 */
#include <zephyr/kernel.h>
#include "biped_motion_state.h"

static struct biped_motion_state_ctx {
    enum biped_motion_state_state state;
} biped_motion_state_instance;

static void biped_motion_state_entry_action(enum biped_motion_state_state state)
{
    switch (state) {
    case BIPED_MOTION_STATE_STATE_DISARMED:
        /* entry: servo power disabled */
        break;
    case BIPED_MOTION_STATE_STATE_CALIBRATE:
        /* entry: load and verify servo centers */
        break;
    case BIPED_MOTION_STATE_STATE_STAND:
        /* entry: ramp to neutral standing pose */
        break;
    case BIPED_MOTION_STATE_STATE_WALK_FORWARD:
        /* entry: start phased gait */
        break;
    case BIPED_MOTION_STATE_STATE_TURN_LEFT:
        /* entry: start left turn gait */
        break;
    case BIPED_MOTION_STATE_STATE_TURN_RIGHT:
        /* entry: start right turn gait */
        break;
    case BIPED_MOTION_STATE_STATE_STOP:
        /* entry: finish step and hold neutral */
        break;
    case BIPED_MOTION_STATE_STATE_FALLEN:
        /* entry: disable gait and servo torque */
        break;
    case BIPED_MOTION_STATE_STATE_FAULT:
        /* entry: latch fault and disable servo power */
        break;
    default: break;
    }
}

static void biped_motion_state_exit_action(enum biped_motion_state_state state)
{
    switch (state) {
    case BIPED_MOTION_STATE_STATE_DISARMED:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_CALIBRATE:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_STAND:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_WALK_FORWARD:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_TURN_LEFT:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_TURN_RIGHT:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_STOP:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_FALLEN:
        /* no exit action */
        break;
    case BIPED_MOTION_STATE_STATE_FAULT:
        /* no exit action */
        break;
    default: break;
    }
}

int biped_motion_state_send_event(enum biped_motion_state_event event)
{
    struct biped_motion_state_ctx *ctx = &biped_motion_state_instance;
    /* calibrate: DISARMED -> CALIBRATE */
    if (ctx->state == BIPED_MOTION_STATE_STATE_DISARMED && event == BIPED_MOTION_STATE_EVT_CALIBRATE) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_CALIBRATE;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* calibration_ok: CALIBRATE -> STAND */
    if (ctx->state == BIPED_MOTION_STATE_STATE_CALIBRATE && event == BIPED_MOTION_STATE_EVT_CALIBRATION_OK) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_STAND;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* walk: STAND -> WALK_FORWARD */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STAND && event == BIPED_MOTION_STATE_EVT_WALK) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_WALK_FORWARD;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* turn_left: STAND -> TURN_LEFT */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STAND && event == BIPED_MOTION_STATE_EVT_TURN_LEFT) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_TURN_LEFT;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* turn_right: STAND -> TURN_RIGHT */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STAND && event == BIPED_MOTION_STATE_EVT_TURN_RIGHT) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_TURN_RIGHT;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* stop: WALK_FORWARD -> STOP */
    if (ctx->state == BIPED_MOTION_STATE_STATE_WALK_FORWARD && event == BIPED_MOTION_STATE_EVT_STOP) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_STOP;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* stop: TURN_LEFT -> STOP */
    if (ctx->state == BIPED_MOTION_STATE_STATE_TURN_LEFT && event == BIPED_MOTION_STATE_EVT_STOP) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_STOP;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* stop: TURN_RIGHT -> STOP */
    if (ctx->state == BIPED_MOTION_STATE_STATE_TURN_RIGHT && event == BIPED_MOTION_STATE_EVT_STOP) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_STOP;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* settled: STOP -> STAND */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STOP && event == BIPED_MOTION_STATE_EVT_SETTLED) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_STAND;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* fall_detected: STAND -> FALLEN */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STAND && event == BIPED_MOTION_STATE_EVT_FALL_DETECTED) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_FALLEN;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* fall_detected: WALK_FORWARD -> FALLEN */
    if (ctx->state == BIPED_MOTION_STATE_STATE_WALK_FORWARD && event == BIPED_MOTION_STATE_EVT_FALL_DETECTED) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_FALLEN;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* reset: FALLEN -> DISARMED */
    if (ctx->state == BIPED_MOTION_STATE_STATE_FALLEN && event == BIPED_MOTION_STATE_EVT_RESET) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_DISARMED;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* fault: DISARMED -> FAULT */
    if (ctx->state == BIPED_MOTION_STATE_STATE_DISARMED && event == BIPED_MOTION_STATE_EVT_FAULT) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_FAULT;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* fault: STAND -> FAULT */
    if (ctx->state == BIPED_MOTION_STATE_STATE_STAND && event == BIPED_MOTION_STATE_EVT_FAULT) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_FAULT;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* fault: WALK_FORWARD -> FAULT */
    if (ctx->state == BIPED_MOTION_STATE_STATE_WALK_FORWARD && event == BIPED_MOTION_STATE_EVT_FAULT) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_FAULT;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    /* reset: FAULT -> DISARMED */
    if (ctx->state == BIPED_MOTION_STATE_STATE_FAULT && event == BIPED_MOTION_STATE_EVT_RESET) {
        biped_motion_state_exit_action(ctx->state);
        ctx->state = BIPED_MOTION_STATE_STATE_DISARMED;
        biped_motion_state_entry_action(ctx->state);
        return 0;
    }
    return -EINVAL;
}

enum biped_motion_state_state biped_motion_state_get_state(void)
{
    return biped_motion_state_instance.state;
}

void biped_motion_state_init(void)
{
    biped_motion_state_instance.state = BIPED_MOTION_STATE_STATE_DISARMED;
    biped_motion_state_entry_action(biped_motion_state_instance.state);
}
