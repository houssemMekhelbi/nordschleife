-- Nordschleife tag look and feel.
-- The instrument cluster by day:
-- anthracite, aluminium, white numerals, one orange needle on the thing that
-- has focus. Right angles only, so windows are sharp. The focused window's 1px
-- border starts in the needle orange at its corner, runs into aluminium and
-- fades; the others get a hairline. No glow: orange is a needle, never a light.
-- Loaded after futuwwa.lua so these values win; behaviour and binds stay there.
-- The popups and helpers are shared by both Nordschleife variants (nordschleife-*).

local C = {
    ground = "E9EBEE",
    line   = "B9BEC6",
    orange = "FF6A1A",
    alu    = "2B2F35",
    fade   = "9AA0A9",
}

hl.config({
    general = {
        gaps_in     = 6,
        gaps_out    = 14,
        border_size = 1,
        col = {
            active_border   = {
                colors = { "rgb(" .. C.orange .. ")", "rgb(" .. C.alu .. ")", "rgb(" .. C.alu .. ")", "rgb(" .. C.fade .. ")", "rgb(" .. C.fade .. ")" },
                angle  = 45,
            },
            inactive_border = "rgb(" .. C.line .. ")",
        },
    },

    decoration = {
        rounding       = 0,
        rounding_power = 2.0,

        active_opacity   = 0.97,
        inactive_opacity = 0.93,

        blur = {
            enabled           = true,
            size              = 8,
            passes            = 3,
            vibrancy          = 0.0,
            noise             = 0.02,
            new_optimizations = true,
            popups            = true,
        },

        glow = {
            enabled = false,
        },

        -- A plain drop shadow; nothing on this desktop glows.
        shadow = {
            enabled        = true,
            range          = 18,
            render_power   = 3,
            offset         = { 0, 6 },
            color          = "rgba(0F11132A)",
            color_inactive = "rgba(0F11132A)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.alu .. ")",
            border_inactive = "rgb(" .. C.line .. ")",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.ground .. ")",
    },
})

-- Cursor: NordschleifeTagNadel (~/.local/share/icons/NordschleifeTagNadel, hyprcursor + XCursor).
-- On a live theme switch restore.sh runs `hyprctl setcursor` from gsettings.txt.
hl.env("HYPRCURSOR_THEME", "NordschleifeTagNadel")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "NordschleifeTagNadel")
hl.env("XCURSOR_SIZE", "24")

-- A config reload resets the cursor to the default theme; set it again.
local function nordschleife_cursor()
    hl.exec_cmd("hyprctl setcursor NordschleifeTagNadel 24")
end
hl.on("hyprland.start", nordschleife_cursor)
hl.on("config.reloaded", nordschleife_cursor)

-- Launcher bind points at the Nordschleife launcher; futuwwa.lua binds the Girih one.
hl.unbind("SUPER + D")
hl.bind("SUPER + D",
    hl.dsp.exec_cmd(os.getenv("HOME") .. "/.local/bin/nordschleife-launcher"),
    { description = "Application launcher" })

-- Terminals draw their own glass (foot/alacritty/ghostty alpha) so text stays opaque.
hl.window_rule({
    name    = "nordschleife-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Blur behind layer surfaces: the bar, alert banners, launcher, notifications.
-- ignore_alpha keeps fully transparent parts of a layer unblurred.
hl.layer_rule({
    name         = "nordschleife-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "nordschleife-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "nordschleife-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/nordschleife-launcher).
hl.window_rule({
    name     = "nordschleife-launcher",
    match    = { class = "^nordschleife-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/nordschleife-yawm).
hl.window_rule({
    name     = "nordschleife-yawm",
    match    = { class = "^nordschleife-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "nordschleife-yawm-add",
    match    = { class = "^nordschleife-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

local nordschleife_popups = { "nordschleife-launcher", "nordschleife-yawm", "nordschleife-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function nordschleife_close_popups(keep)
    for _, class in ipairs(nordschleife_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function nordschleife_close_launcher()
    nordschleife_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    nordschleife_close_popups(win and win.class)
end)
