local function run_pytest()
    -- Remember the window we started in
    local orig_win = vim.api.nvim_get_current_win()

    -- Navigate to bottom-left window
    vim.cmd("wincmd h")
    vim.cmd("wincmd j")

    -- Capture the destination window
    local target_win = vim.api.nvim_get_current_win()

    vim.schedule(function()
        if not vim.api.nvim_win_is_valid(target_win) then
            return
        end

        vim.api.nvim_set_current_win(target_win)
        vim.api.nvim_input("i")
        vim.api.nvim_input("clear && lint-imports && python -m pytest<CR>")

        -- Return after the command has been submitted
        vim.schedule(function()
            if vim.api.nvim_win_is_valid(orig_win) then
                vim.api.nvim_set_current_win(orig_win)
            end
        end)
    end)
end

vim.keymap.set("n", "0-", function()
    run_pytest()
end, { desc = "Run pytest" })
