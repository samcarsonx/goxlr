import ctypes
from .ws import Socket
from .types import *

# Based off of this file:
# https://github.com/GoXLR-on-Linux/goxlr-utility/blob/f2a5c1b22080c7cfb2a096efde23913a149b657a/ipc/src/lib.rs


class GoXLR(Socket):
    def __init__(self, host="localhost", port=14564):
        super().__init__(host, port)

    # General commands

    async def ping(self):
        return await self.send("Ping")

    async def get_status(self):
        return await self.send("GetStatus")

    # Daemon commands

    async def __send_daemon(self, payload):
        payload = {"Daemon": payload}
        return await self.send(payload)

    async def open_ui(self):
        return await self.__send_daemon("OpenUi")

    async def activate(self):
        return await self.__send_daemon("Activate")

    async def stop_daemon(self):
        return await self.__send_daemon("StopDaemon")

    async def open_path(self, pathType: PathTypes):
        return await self.__send_daemon({"OpenPath": pathType.name})

    async def set_log_level(self, logLevel: LogLevel):
        return await self.__send_daemon({"SetLogLevel": logLevel.name})

    async def set_show_tray_icon(self, enabled: bool):
        return await self.__send_daemon({"SetShowTrayIcon": enabled})

    async def set_tts_enabled(self, enabled: bool):
        return await self.__send_daemon({"SetTTSEnabled": enabled})

    async def set_auto_start_enabled(self, enabled: bool):
        return await self.__send_daemon({"SetAutoStartEnabled": enabled})

    async def set_allow_network_access(self, enabled: bool):
        return await self.__send_daemon({"SetAllowNetworkAccess": enabled})

    async def recover_defaults(self, pathType: PathTypes):
        return await self.__send_daemon({"RecoverDefaults": pathType.name})

    # GoXLR commands

    async def __send_command(self, payload, serial=None):
        payload = {"Command": [serial or self.serial, payload]}
        return await self.send(payload)

    async def set_shutdown_commands(self, *commands):
        # I'm not sure how this works in the API, so I'm just going to leave it for now
        # Plus I don't know how I'd make it work with the rest of my wrapper yet
        pass

    async def set_sampler_pre_buffer_duration(self, duration: ctypes.c_uint16):
        return await self.__send_command({"SetSamplerPreBufferDuration": duration})

    async def set_fader(self, fader_name: FaderName, channel_name: ChannelName):
        return await self.__send_command(
            {"SetFader": [fader_name.name, channel_name.name]}
        )

    async def set_fader_mute_function(
        self, fader_name: FaderName, mute_function: MuteFunction
    ):
        return await self.__send_command(
            {"SetFaderMuteFunction": [fader_name.name, mute_function.name]}
        )

    async def set_volume(self, channel_name: ChannelName, volume: ctypes.c_uint8):
        return await self.__send_command({"SetVolume": [channel_name.name, volume]})

    async def set_microphone_type(self, microphone_type: MicrophoneType):
        return await self.__send_command({"SetMicrophoneType": microphone_type.name})

    async def set_microphone_gain(
        self, microphone_type: MicrophoneType, gain: ctypes.c_uint16
    ):
        return await self.__send_command(
            {"SetMicrophoneGain": [microphone_type.name, gain]}
        )

    async def set_router(
        self, input_device: InputDevice, output_device: OutputDevice, enabled: bool
    ):
        return await self.__send_command(
            {"SetRouter": [input_device.name, output_device.name, enabled]}
        )

    # Cough Button
    async def set_cough_mute_function(self, mute_function: MuteFunction):
        return await self.__send_command({"SetCoughMuteFunction": mute_function.name})

    async def set_cough_is_hold(self, is_hold: bool):
        return await self.__send_command({"SetCoughIsHold": is_hold})

    # Bleep Button
    async def set_swear_button_volume(self, volume: ctypes.c_int8):
        return await self.__send_command({"SetSwearButtonVolume": volume})

    # EQ Settings
    async def set_eq_mini_gain(
        self, mini_eq_frequency: MiniEqFrequencies, gain: ctypes.c_int8
    ):
        return await self.__send_command(
            {"SetEqMiniGain": [mini_eq_frequency.name, gain]}
        )

    async def set_eq_mini_frequency(
        self, mini_eq_frequency: MiniEqFrequencies, frequency: ctypes.c_float
    ):
        return await self.__send_command(
            {"SetEqMiniFrequency": [mini_eq_frequency.name, frequency]}
        )

    async def set_eq_gain(self, eq_frequency: EqFrequencies, gain: ctypes.c_int8):
        return await self.__send_command({"SetEqGain": [eq_frequency.name, gain]})

    async def set_eq_frequency(
        self, eq_frequency: EqFrequencies, frequency: ctypes.c_float
    ):
        return await self.__send_command(
            {"SetEqFrequency": [eq_frequency.name, frequency]}
        )

    # Gate Settings
    async def set_gate_threshold(self, gate_threshold: ctypes.c_int8):
        return await self.__send_command({"SetGateThreshold": gate_threshold})

    async def set_gate_attenuation(self, gate_attenuation: ctypes.c_uint8):
        return await self.__send_command({"SetGateAttenuation": gate_attenuation})

    async def set_gate_attack(self, gate_attack: GateTimes):
        return await self.__send_command({"SetGateAttack": gate_attack.name})

    async def set_gate_release(self, gate_release: GateTimes):
        return await self.__send_command({"SetGateRelease": gate_release.name})

    async def set_gate_active(self, gate_active: bool):
        return await self.__send_command({"SetGateActive": gate_active})

    # Compressor Settings
    async def set_compressor_threshold(self, compressor_threshold: ctypes.c_int8):
        return await self.__send_command(
            {"SetCompressorThreshold": compressor_threshold}
        )

    async def set_compressor_ratio(self, compressor_ratio: CompressorRatio):
        return await self.__send_command({"SetCompressorRatio": compressor_ratio.name})

    async def set_compressor_attack(self, compressor_attack: CompressorAttackTime):
        return await self.__send_command(
            {"SetCompressorAttack": compressor_attack.name}
        )

    async def set_compressor_release_time(
        self, compressor_release: CompressorReleaseTime
    ):
        return await self.__send_command(
            {"SetCompressorReleaseTime": compressor_release.name}
        )

    async def set_compressor_makeup_gain(self, compressor_makeup_gain: ctypes.c_int8):
        return await self.__send_command(
            {"SetCompressorMakeupGain": compressor_makeup_gain}
        )

    # Used to switch between display modes
    async def set_element_display_mode(
        self, display_mode_components: DisplayModeComponents, display_mode: DisplayMode
    ):
        return await self.__send_command(
            {"SetElementDisplayMode": [display_mode_components.name, display_mode.name]}
        )

    # DeEss
    async def set_deeser(self, deesser: ctypes.c_uint8):
        return await self.__send_command({"SetDeesser": deesser})

    # Colour Related Settings
    async def set_animation_mode(self, animation_mode: AnimationMode):
        return await self.__send_command({"SetAnimationMode": animation_mode.name})

    async def set_animation_mod1(self, animation_mod1: ctypes.c_uint8):
        return await self.__send_command({"SetAnimationMod1": animation_mod1})

    async def set_animation_mod2(self, animation_mod2: ctypes.c_uint8):
        return await self.__send_command({"SetAnimationMod2": animation_mod2})

    async def set_animation_waterfall(self, waterfall_direction: WaterfallDirection):
        return await self.__send_command(
            {"SetAnimationWaterfall": waterfall_direction.name}
        )

    async def set_global_colour(self, colour: str):
        return await self.__send_command({"SetGlobalColour": colour})

    async def set_fader_display_style(
        self, fader_name: FaderName, fader_display_style: FaderDisplayStyle
    ):
        return await self.__send_command(
            {"SetFaderDisplayStyle": [fader_name.name, fader_display_style.name]}
        )

    async def set_fader_colours(
        self, fader_name: FaderName, colour1: str, colour2: str
    ):
        return await self.__send_command(
            {"SetFaderColours": [fader_name.name, colour1, colour2]}
        )

    async def set_all_fader_colours(self, colour1: str, colour2: str):
        return await self.__send_command({"SetAllFaderColours": [colour1, colour2]})

    async def set_all_fader_display_style(self, fader_display_style: FaderDisplayStyle):
        return await self.__send_command(
            {"SetAllFaderDisplayStyle": fader_display_style.name}
        )

    async def set_button_colours(
        self, button_name: Button, colour1: str, colour2: str = None
    ):
        return await self.__send_command(
            {"SetButtonColours": [button_name.name, colour1, colour2]}
        )

    async def set_button_off_style(
        self, button_name: Button, off_style: ButtonColourOffStyle
    ):
        return await self.__send_command(
            {"SetButtonOffStyle": [button_name.name, off_style.name]}
        )

    async def set_button_group_colours(
        self,
        button_colour_groups: ButtonColourGroups,
        colour1: str,
        colour2: str = None,
    ):
        return await self.__send_command(
            {"SetButtonGroupColours": [button_colour_groups.name, colour1, colour2]}
        )

    async def set_button_group_off_style(
        self, button_colour_groups: ButtonColourGroups, off_style: ButtonColourOffStyle
    ):
        return await self.__send_command(
            {"SetButtonGroupOffStyle": [button_colour_groups.name, off_style.name]}
        )

    async def set_simple_colour(
        self, simple_colour_targets: SimpleColourTargets, colour: str
    ):
        return await self.__send_command(
            {"SetSimpleColour": [simple_colour_targets.name, colour]}
        )

    async def set_encoder_colour(self, encoder_name: EncoderColourTargets, colour: str):
        return await self.__send_command(
            {"SetEncoderColour": [encoder_name.name, colour]}
        )

    async def set_sample_colour(self, sample_name: SamplerColourTargets, colour: str):
        return await self.__send_command(
            {"SetSampleColour": [sample_name.name, colour]}
        )

    async def set_sample_off_style(
        self, sample_name: SamplerColourTargets, off_style: ButtonColourOffStyle
    ):
        return await self.__send_command(
            {"SetSampleOffStyle": [sample_name.name, off_style.name]}
        )

    # Effect Related Settings
    async def load_effect(self, effect_name: str):
        return await self.__send_command({"LoadEffect": effect_name})

    async def rename_active_preset(self, new_name: str):
        return await self.__send_command({"RenameActivePreset": new_name})

    async def save_active_preset(self):
        return await self.__send_command({"SaveActivePreset": []})

    # Reverb
    async def set_reverb_style(self, reverb_style: ReverbStyle):
        return await self.__send_command({"SetReverbStyle": reverb_style.name})

    async def set_reverb_amount(self, reverb_amount: ctypes.c_uint8):
        return await self.__send_command({"SetReverbAmount": reverb_amount})

    async def set_reverb_decay(self, reverb_decay: ctypes.c_uint16):
        return await self.__send_command({"SetReverbDecay": reverb_decay})

    async def set_reverb_early_level(self, reverb_early_level: ctypes.c_int8):
        return await self.__send_command({"SetReverbEarlyLevel": reverb_early_level})

    async def set_reverb_tail_level(self, reverb_tail_level: ctypes.c_int8):
        return await self.__send_command({"SetReverbTailLevel": reverb_tail_level})

    async def set_reverb_pre_delay(self, reverb_pre_delay: ctypes.c_uint8):
        return await self.__send_command({"SetReverbPreDelay": reverb_pre_delay})

    async def set_reverb_low_colour(self, reverb_low_colour: ctypes.c_int8):
        return await self.__send_command({"SetReverbLowColour": reverb_low_colour})

    async def set_reverb_high_colour(self, reverb_high_colour: ctypes.c_int8):
        return await self.__send_command({"SetReverbHighColour": reverb_high_colour})

    async def set_reverb_high_factor(self, reverb_high_factor: ctypes.c_int8):
        return await self.__send_command({"SetReverbHighFactor": reverb_high_factor})

    async def set_reverb_diffuse(self, reverb_diffuse: ctypes.c_uint8):
        return await self.__send_command({"SetReverbDiffuse": reverb_diffuse})

    async def set_reverb_mod_speed(self, reverb_mod_speed: ctypes.c_uint8):
        return await self.__send_command({"SetReverbModSpeed": reverb_mod_speed})

    async def set_reverb_mod_depth(self, reverb_mod_depth: ctypes.c_uint8):
        return await self.__send_command({"SetReverbModDepth": reverb_mod_depth})

    # Echo
    async def set_echo_style(self, echo_style: EchoStyle):
        return await self.__send_command({"SetEchoStyle": echo_style.name})

    async def set_echo_amount(self, echo_amount: ctypes.c_uint8):
        return await self.__send_command({"SetEchoAmount": echo_amount})

    async def set_echo_feedback(self, echo_feedback: ctypes.c_uint8):
        return await self.__send_command({"SetEchoFeedback": echo_feedback})

    async def set_echo_tempo(self, echo_tempo: ctypes.c_uint16):
        return await self.__send_command({"SetEchoTempo": echo_tempo})

    async def set_echo_delay_left(self, echo_delay_left: ctypes.c_uint16):
        return await self.__send_command({"SetEchoDelayLeft": echo_delay_left})

    async def set_echo_delay_right(self, echo_delay_right: ctypes.c_uint16):
        return await self.__send_command({"SetEchoDelayRight": echo_delay_right})

    async def set_echo_feedback_left(self, echo_feedback_left: ctypes.c_uint8):
        return await self.__send_command({"SetEchoFeedbackLeft": echo_feedback_left})

    async def set_echo_feedback_right(self, echo_feedback_right: ctypes.c_uint8):
        return await self.__send_command({"SetEchoFeedbackRight": echo_feedback_right})

    async def set_echo_feedback_xfb_l_to_r(
        self, echo_feedback_xfb_l_to_r: ctypes.c_uint8
    ):
        return await self.__send_command(
            {"SetEchoFeedbackXFBLtoR": echo_feedback_xfb_l_to_r}
        )

    async def set_echo_feedback_xfb_r_to_l(
        self, echo_feedback_xfb_r_to_l: ctypes.c_uint8
    ):
        return await self.__send_command(
            {"SetEchoFeedbackXFBRtoL": echo_feedback_xfb_r_to_l}
        )

    # Pitch
    async def set_pitch_style(self, pitch_style: PitchStyle):
        return await self.__send_command({"SetPitchStyle": pitch_style.name})

    async def set_pitch_amount(self, pitch_amount: ctypes.c_int8):
        return await self.__send_command({"SetPitchAmount": pitch_amount})

    async def set_pitch_character(self, pitch_character: ctypes.c_uint8):
        return await self.__send_command({"SetPitchCharacter": pitch_character})

    # Gender
    async def set_gender_style(self, gender_style: GenderStyle):
        return await self.__send_command({"SetGenderStyle": gender_style.name})

    async def set_gender_amount(self, gender_amount: ctypes.c_int8):
        return await self.__send_command({"SetGenderAmount": gender_amount})

    # Megaphone
    async def set_megaphone_style(self, megaphone_style: MegaphoneStyle):
        return await self.__send_command({"SetMegaphoneStyle": megaphone_style.name})

    async def set_megaphone_amount(self, megaphone_amount: ctypes.c_uint8):
        return await self.__send_command({"SetMegaphoneAmount": megaphone_amount})

    async def set_megaphone_post_gain(self, megaphone_post_gain: ctypes.c_int8):
        return await self.__send_command({"SetMegaphonePostGain": megaphone_post_gain})

    # Robot
    async def set_robot_style(self, robot_style: RobotStyle):
        return await self.__send_command({"SetRobotStyle": robot_style.name})

    async def set_robot_gain(self, robot_range: RobotRange, robot_gain: ctypes.c_int8):
        return await self.__send_command(
            {"SetRobotGain": [robot_range.name, robot_gain]}
        )

    async def set_robot_frequency(
        self, robot_range: RobotRange, robot_frequency: ctypes.c_uint8
    ):
        return await self.__send_command(
            {"SetRobotFreq": [robot_range.name, robot_frequency]}
        )

    async def set_robot_width(
        self, robot_range: RobotRange, robot_width: ctypes.c_uint8
    ):
        return await self.__send_command(
            {"SetRobotWidth": [robot_range.name, robot_width]}
        )

    async def set_robot_waveform(self, robot_waveform: ctypes.uint8):
        return await self.__send_command({"SetRobotWaveform": robot_waveform})

    async def set_robot_pulse_width(self, robot_pulse_width: ctypes.c_uint8):
        return await self.__send_command({"SetRobotPulseWidth": robot_pulse_width})

    async def set_robot_threshold(self, robot_threshold: ctypes.c_int8):
        return await self.__send_command({"SetRobotThreshold": robot_threshold})

    async def set_robot_dry_mix(self, robot_dry_mix: ctypes.c_int8):
        return await self.__send_command({"SetRobotDryMix": robot_dry_mix})

    # Hardtune
    async def set_hardtune_style(self, hardtune_style: HardTuneStyle):
        return await self.__send_command({"SetHardTuneStyle": hardtune_style.name})

    async def set_hardtune_amount(self, hardtune_amount: ctypes.c_uint8):
        return await self.__send_command({"SetHardTuneAmount": hardtune_amount})

    async def set_hardtune_rate(self, hardtune_rate: ctypes.c_uint8):
        return await self.__send_command({"SetHardTuneRate": hardtune_rate})

    async def set_hardtune_window(self, hardtune_window: ctypes.c_uint16):
        return await self.__send_command({"SetHardTuneWindow": hardtune_window})

    async def set_hardtune_source(self, hardtune_source: HardTuneSource):
        return await self.__send_command({"SetHardTuneSource": hardtune_source.name})

    # Sampler
    async def clear_sample_process_error(self):
        return await self.__send_command({"ClearSampleProcessError": []})

    async def set_sampler_function(
        self,
        sample_bank: SampleBank,
        sample_buttons: SampleButtons,
        sample_playback_mode: SamplePlaybackMode,
    ):
        return await self.__send_command(
            {
                "SetSamplerFunction": [
                    sample_bank.name,
                    sample_buttons.name,
                    sample_playback_mode.name,
                ]
            }
        )

    async def set_sampler_order(
        self,
        sample_bank: SampleBank,
        sample_buttons: SampleButtons,
        sample_play_order: SamplePlayOrder,
    ):
        return await self.__send_command(
            {
                "SetSamplerOrder": [
                    sample_bank.name,
                    sample_buttons.name,
                    sample_play_order.name,
                ]
            }
        )

    async def add_sample(
        self, sample_bank: SampleBank, sample_buttons: SampleButtons, sample_name: str
    ):
        return await self.__send_command(
            {"AddSample": [sample_bank.name, sample_buttons.name, sample_name]}
        )

    async def set_sample_start_percent(
        self,
        sample_bank: SampleBank,
        sample_buttons: SampleButtons,
        index: int,
        sample_start_percent: ctypes.c_float,
    ):
        return await self.__send_command(
            {
                "SetSampleStartPercent": [
                    sample_bank.name,
                    sample_buttons.name,
                    index,
                    sample_start_percent,
                ]
            }
        )

    async def set_sample_stop_percent(
        self,
        sample_bank: SampleBank,
        sample_buttons: SampleButtons,
        index: int,
        sample_stop_percent: ctypes.c_float,
    ):
        return await self.__send_command(
            {
                "SetSampleStopPercent": [
                    sample_bank.name,
                    sample_buttons.name,
                    index,
                    sample_stop_percent,
                ]
            }
        )

    async def remove_sample_by_index(
        self, sample_bank: SampleBank, sample_buttons: SampleButtons, index: int
    ):
        return await self.__send_command(
            {"RemoveSampleByIndex": [sample_bank.name, sample_buttons.name, index]}
        )

    async def play_sample_by_index(
        self, sample_bank: SampleBank, sample_buttons: SampleButtons, index: int
    ):
        return await self.__send_command(
            {"PlaySampleByIndex": [sample_bank.name, sample_buttons.name, index]}
        )

    async def play_next_sample(
        self, sample_bank: SampleBank, sample_buttons: SampleButtons
    ):
        return await self.__send_command(
            {"PlayNextSample": [sample_bank.name, sample_buttons.name]}
        )

    async def stop_sample_playback(
        self, sample_bank: SampleBank, sample_buttons: SampleButtons
    ):
        return await self.__send_command(
            {"StopSamplePlayback": [sample_bank.name, sample_buttons.name]}
        )

    # Scribbles
    async def set_scribble_icon(self, fader_name: FaderName, scribble_icon: str = None):
        return await self.__send_command(
            {"SetScribbleIcon": [fader_name.name, scribble_icon]}
        )

    async def set_scribble_text(self, fader_name: FaderName, scribble_text: str):
        return await self.__send_command(
            {"SetScribbleText": [fader_name.name, scribble_text]}
        )

    async def set_scribble_number(self, fader_name: FaderName, scribble_number: str):
        return await self.__send_command(
            {"SetScribbleNumber": [fader_name.name, scribble_number]}
        )

    async def set_scribble_invert(self, fader_name: FaderName, scribble_invert: bool):
        return await self.__send_command(
            {"SetScribbleInvert": [fader_name.name, scribble_invert]}
        )

    # Profile Handling
    async def new_profile(self, profile_name: str):
        return await self.__send_command({"NewProfile": profile_name})

    async def load_profile(self, profile_name: str, save_changes: bool = False):
        return await self.__send_command({"LoadProfile": [profile_name, save_changes]})

    async def load_profile_colours(self, profile_name: str):
        return await self.__send_command({"LoadProfileColours": profile_name})

    async def save_profile(self):
        return await self.__send_command({"SaveProfile": []})

    async def save_profile_as(self, profile_name: str):
        return await self.__send_command({"SaveProfileAs": profile_name})

    async def delete_profile(self, profile_name: str):
        return await self.__send_command({"DeleteProfile": profile_name})

    async def new_mic_profile(self, profile_name: str):
        return await self.__send_command({"NewMicProfile": profile_name})

    async def load_mic_profile(self, profile_name: str, save_changes: bool = False):
        return await self.__send_command(
            {"LoadMicProfile": [profile_name, save_changes]}
        )

    async def save_mic_profile(self):
        return await self.__send_command({"SaveMicProfile": []})

    async def save_mic_profile_as(self, profile_name: str):
        return await self.__send_command({"SaveMicProfileAs": profile_name})

    async def delete_mic_profile(self, profile_name: str):
        return await self.__send_command({"DeleteMicProfile": profile_name})

    # General Settings
    async def set_mute_hold_duration(self, mute_hold_duration: ctypes.c_uint16):
        return await self.__send_command({"SetMuteHoldDuration": mute_hold_duration})

    async def set_vc_mute_also_mute_cm(self, vc_mute_also_mute_cm: bool):
        return await self.__send_command({"SetVCMuteAlsoMuteCM": vc_mute_also_mute_cm})

    # These control the current GoXLR state
    async def set_active_effect_preset(self, active_effect_preset: EffectBankPresets):
        return await self.__send_command(
            {"SetActiveEffectPreset": active_effect_preset.name}
        )

    async def set_active_sampler_bank(self, active_sampler_bank: SampleBank):
        return await self.__send_command(
            {"SetActiveSamplerBank": active_sampler_bank.name}
        )

    async def set_megaphone_enabled(self, megaphone_enabled: bool):
        return await self.__send_command({"SetMegaphoneEnabled": megaphone_enabled})

    async def set_robot_enabled(self, robot_enabled: bool):
        return await self.__send_command({"SetRobotEnabled": robot_enabled})

    async def set_hardtune_enabled(self, hardtune_enabled: bool):
        return await self.__send_command({"SetHardTuneEnabled": hardtune_enabled})

    async def set_fx_enabled(self, fx_enabled: bool):
        return await self.__send_command({"SetFXEnabled": fx_enabled})

    async def set_fader_mute_state(self, fader_name: FaderName, mute_state: MuteState):
        return await self.__send_command(
            {"SetFaderMuteState": [fader_name.name, mute_state.name]}
        )

    async def set_cough_mute_state(self, mute_state: MuteState):
        return await self.__send_command({"SetCoughMuteState": mute_state.name})

    # Submix commands
    async def set_submix_enabled(self, enabled: bool):
        return await self.__send_command({"SetSubMixEnabled": enabled})

    async def set_submix_volume(
        self, channel_name: ChannelName, volume: ctypes.c_uint8
    ):
        return await self.__send_command(
            {"SetSubMixVolume": [channel_name.name, volume]}
        )

    async def set_submix_linked(self, channel_name: ChannelName, linked: bool):
        return await self.__send_command(
            {"SetSubMixLinked": [channel_name.name, linked]}
        )

    async def set_submix_output_mix(self, output_device: OutputDevice, mix: Mix):
        return await self.__send_command(
            {"SetSubMixOutputMix": [output_device.name, mix.name]}
        )

    # Mix monitoring
    async def set_monitor_mix(self, output_device: OutputDevice):
        return await self.__send_command({"SetMonitorMix": output_device.name})

    # it's..done..?
