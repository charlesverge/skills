# Plan Completion Review Report

## 1. Run tests, linters

### pytest

- None

### Playwright

- Failure: `npx playwright test e2e/mock_jobs.spec.ts`
  - Error: 6 failed, 0 passed. All failures stop at `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/mock_jobs.spec.ts:163`, waiting for text `Practice` after `/agents?start_calibration=1`.
  - Evidence: Browser validation for the mock calibration plans is not passing.
- Failure: `npx playwright test e2e/real_jobs.spec.ts`
  - Error: 14 failed, 8 passed.
  - Evidence: Passed browser coverage includes no-results, broaden criteria, completion, reconnect, expand/collapse, retry search, ignore, and posting open. Failed cases include calibration handoff, real-search start, recommendation retry, next-step search UI, apply request, save/favorite flows.

### Linters

- Failure: `npm run lint -- --file app/agents/page.tsx --file app/(account)/searching/SearchingScreen.tsx --file components/chat/JobCard.tsx`
  - Error: `package.json` has no `lint` script.
  - Evidence: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/package.json` does not define lint.

### Type checks

- Success: `npx tsc --noEmit`
  - Error:
  - Evidence: Command exited 0.

### Build or runtime checks

- Success: `npm test -- SearchingScreen.test.tsx`
  - Error:
  - Evidence: 47 passed.
- Success: `npm test -- ChatShell.test.tsx`
  - Error:
  - Evidence: 104 passed, with React `act(...)` warnings.
- Failure: `npm test -- app/agents/page.test.tsx components/chat/JobCard.test.tsx`
  - Error: 1 failed, 57 passed. `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.test.tsx:830` queries button name `Apply`; actual accessible name is `Apply for Principal Product Manager`.
  - Evidence: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/components/chat/JobCard.tsx:210`.

## 2. Review code for unexpected side effects

- Finding: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx:858` `startRealSearch`
  - Side effect category: Missing required API side effect
  - Impact: Real-search start can route to `/searching` without first calling `POST /api/v1/jobs/search/start`.
  - Evidence: `startRealSearch` only calls `setJobMode("real")` and `router.push("/searching")`.
  - Required change: Add the plan-required search-start request before route transition.
- Finding: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.tsx:705`
  - Side effect category: Incomplete planned ownership path
  - Impact: `search-calibrate.md` requires `ChatShell` to invoke the mock-job request and render the returned deck. `ChatShell` only routes to `/agents?start_calibration=1`.
  - Evidence: No `POST /api/v1/jobs/mock` or mock deck rendering exists in `ChatShell.tsx`.
  - Required change: Implement the plan-owned calibration request/deck handoff in `ChatShell.tsx` behind the ChatShell trigger without changing the plan contract.

## 3. Create a list of features and ensure they are all completed

| Feature or requirement                               | Plan source                                            | Status    |
| ---------------------------------------------------- | ------------------------------------------------------ | --------- |
| Back to chat without starting or stopping search     | `plans/features/search-back-to-chat.md`                | Completed |
| Start mock-job calibration from completed onboarding | `plans/features/search-calibrate.md`                   | Partial   |
| Calibration API error state with retry               | `plans/features/search-calibration-error.md`           | Partial   |
| Calibration loading state                            | `plans/features/search-calibration-loading.md`         | Partial   |
| Completed career profile summary after calibration   | `plans/features/search-calibration-profile-summary.md` | Partial   |
| Search chat status navigation                        | `plans/features/search-chat-navigation.md`             | Completed |
| Search complete results state                        | `plans/features/search-complete.md`                    | Completed |
| Search complete no-results state                     | `plans/features/search-complete-no-results.md`         | Completed |
| No-results broaden CTA rendering                     | `plans/features/search-criteria-broaden-no-results.md` | Completed |
| Broaden criteria navigation to onboarding            | `plans/features/search-criteria-broaden.md`            | Completed |
| Apply to real job and open posting                   | `plans/features/search-job-apply.md`                   | Partial   |
| Expand/collapse job description                      | `plans/features/search-job-description-expand.md`      | Completed |
| Mock job Yes/Maybe/No feedback persistence           | `plans/features/search-job-feedback.md`                | Partial   |
| Ignore real job and load/remove recommendation       | `plans/features/search-job-ignore.md`                  | Completed |
| Open external job posting in new tab                 | `plans/features/search-job-posting-open.md`            | Completed |
| Retry recommendation loading after API failure       | `plans/features/search-recommendation-error-retry.md`  | Partial   |
| Retry failed or empty search status flow             | `plans/features/search-retry.md`                       | Completed |
| Review real-job recommendation state                 | `plans/features/search-review-jobs.md`                 | Completed |
| Keep standing search active from no-results          | `plans/features/search-standing-search-keep.md`        | Completed |
| Start real-job search from CTA and route to progress | `plans/features/search-start-real.md`                  | Partial   |
| Reconnect status stream after SSE disconnect         | `plans/features/search-status-reconnect.md`            | Completed |

## 4. Verify the plan is valid. Ensure the original goal has been met with the plan

| Goal description                                                                                                                                                                | In Plan | Short change description                                                    | Has tests |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------- | --------- |
| Combined `search-*` plans cover calibration, real-search start, status streaming, no-results actions, recommendation review, job actions, retry, reconnect, and chat navigation | Full    | Plan set is coherent and directly describes the requested search experience | Yes       |
| Calibration start from completed onboarding in `ChatShell.tsx`                                                                                                                  | Full    | Plan requires `ChatShell` CTA visibility, mock-job request, and deck render | Yes       |
| Real-search start API call before `/searching` route                                                                                                                            | Full    | Plan requires `POST /api/v1/jobs/search/start` before status stream handoff | Yes       |
| Browser verification for mock and real jobs                                                                                                                                     | Full    | Plans require `mock_jobs.spec.ts` and `real_jobs.spec.ts`                   | Yes       |

## 5. Verify the code completes the original goal

| Goal description                                                                                                | File name                                                                                                        | In Code | Short change description                                                                                  | Has tests |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------- | --------- |
| Search status, complete, no-results, retry, reconnect, back-to-chat, broaden, keep standing search, review jobs | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/(account)/searching/SearchingScreen.tsx` | Full    | SSE stream, status states, retry, no-results actions, and recommendation card render are implemented      | Yes       |
| Calibration start from completed onboarding                                                                     | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.tsx`                    | Partial | CTA exists, but the plan-required mock-job request and deck render are not implemented in this file       | Yes       |
| Mock calibration deck, loading, error, feedback, profile summary                                                | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx`                         | Partial | Code exists, but it does not satisfy the plan’s stated implementation owner by itself; browser tests fail | Yes       |
| Shared real/mock job card actions and description expansion                                                     | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/components/chat/JobCard.tsx`                 | Full    | Card fields, mock feedback buttons, real actions, posting link, and expand/collapse are implemented       | Yes       |
| Search chat status navigation                                                                                   | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/MyRuntimeProvider.tsx`                   | Full    | Search-scoped `ui_command` navigation routes to `/searching`                                              | Yes       |
| Real-search start from calibration complete                                                                     | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx`                         | Partial | Routes to `/searching`, but does not call `POST /api/v1/jobs/search/start` first                          | Yes       |
| Plan-required browser tests                                                                                     | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/mock_jobs.spec.ts`                       | Partial | Spec exists, but all tests fail                                                                           | Yes       |
| Plan-required browser tests                                                                                     | `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts`                       | Partial | Spec exists, but 14 of 22 tests fail                                                                      | Yes       |

## 6. What are the unrequested modifications made

- None

## 7. Is there anything that will fail to execute, or produce the expected outcome

### Runtime failures

- Runtime failure: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/mock_jobs.spec.ts:163` `openMockJobs`
  - Error: Browser tests wait for `Practice`, but the expected element is not found.
  - Evidence: `mock_jobs.spec.ts` 6 failed.
- Runtime failure: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts:199` `completeCalibrationAndOpenRealJobs`
  - Error: Calibration helper fails before real-job flow assertions execute.
  - Evidence: Multiple `real_jobs.spec.ts` failures share this line.
- Runtime failure: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.test.tsx:830`
  - Error: Test cannot find an accessible button named `Apply`.
  - Evidence: Actual button name is `Apply for Principal Product Manager`.

### Incorrect outputs

- Incorrect output: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx:858` `startRealSearch`
  - Expected: Call `POST /api/v1/jobs/search/start`, then route to `/searching`.
  - Actual: Routes to `/searching` without the search-start request.
- Incorrect output: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.tsx:705` `startSearchCalibration`
  - Expected: `ChatShell` starts mock-job calibration and hands the user to a deck with cards from `POST /api/v1/jobs/mock`.
  - Actual: `ChatShell` only pushes `/agents?start_calibration=1`.

### Blocking risks

- Risk: `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts:563`
  - Risk: `getByRole("alert")` resolves both the app alert and Next route announcer.
  - Evidence: Playwright strict mode violation.

## 8. Questions: Is there any thing you are unsure about

- None

## 9. Suggested improvements

- Add a focused unit test in `ChatShell.test.tsx` proving the `Calibrate my search` CTA starts the mock-job request path required by `search-calibrate.md`.
- Add a focused unit test proving `startRealSearch` calls `POST /api/v1/jobs/search/start` before routing.

## 10. Migration

- None

## 11. Assumptions

- The plan files are the source of truth.
- Code that exists outside the files named by the plan is treated as supporting evidence only, not a reason to change the plan.

## 12. Changes required

- **Files needing changes:**
  - Modify:
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.tsx:705`
      - Required change: Update `startSearchCalibration` so activating `Calibrate my search` starts the mock-job calibration flow required by `search-calibrate.md`: request `POST /api/v1/jobs/mock`, show loading while pending, show the calibration deck on success, and show retryable error state on failure.
      - Reason: `search-calibrate.md`, `search-calibration-loading.md`, and `search-calibration-error.md` define this behavior as owned by the chat calibration trigger.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx:858`
      - Required change: Call `POST /api/v1/jobs/search/start` before routing to `/searching`.
      - Reason: `search-start-real.md` requires creating or reusing the current `searches` record before the status stream opens.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.test.tsx:830`
      - Required change: Query the accessible apply button by `Apply for Principal Product Manager`.
      - Reason: The card includes the job title in the accessible name.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/mock_jobs.spec.ts:163`
      - Required change: Fix the calibration entry assertion so the test waits for the actual plan-owned calibration deck state and then verifies Yes, Maybe, and No controls.
      - Reason: Plan-required browser verification currently fails.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts:199`
      - Required change: Fix the shared calibration helper so real-job browser tests can reach their target assertions.
      - Reason: This helper blocks multiple plan-required real-job tests.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts:563`
      - Required change: Scope the recommendation retry alert query to the application alert instead of all `role="alert"` elements.
      - Reason: Current query fails strict mode.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts:687`
      - Required change: Align the expected apply-action request URL with the seeded job id used by the rendered recommendation.
      - Reason: Current request wait times out.
- **Classes, properties, and types needing changes:**
  - None
- **Functions needing changes:**
  - Modify:
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.tsx:705` `startSearchCalibration()`
      - Required change: Implement the plan-required mock-job calibration start flow from the CTA: set calibration loading state, call `POST /api/v1/jobs/mock`, render returned mock jobs as the calibration deck, preserve empty-deck behavior, and surface retryable API errors.
      - Reason: `search-calibrate.md` requires the CTA to render returned mock jobs.
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.tsx:858` `startRealSearch()`
      - Required change: Make the function await `fetch("/api/v1/jobs/search/start", { method: "POST" })` before `setJobMode("real")` and `router.push("/searching")`; do not route until the start request succeeds.
      - Reason: `search-start-real.md` requires the current real search to exist before `/searching`.
- **Constants needing changes:**
  - None
- **Tests needing changes:**
  - Add:
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.test.tsx` `clicking calibrate my search renders returned mock jobs`
      - Required change: Add the plan-required test that mocks `POST /api/v1/jobs/mock` and verifies the returned card renders from the CTA path.
      - Verification: CTA click renders the mock deck.
      - Coverage category: Happy path
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.test.tsx` `calibration deck receives focus after successful load`
      - Required change: Add focus verification for the deck after load.
      - Verification: Deck heading or first card receives focus.
      - Coverage category: Validation or error path
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/ChatShell.test.tsx` `empty mock jobs response does not render calibration deck`
      - Required change: Add the empty-deck test.
      - Verification: Empty `jobs` response does not render a mock card deck.
      - Coverage category: Edge case
  - Modify:
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/app/agents/page.test.tsx` `posts next-steps after a real job is applied`
      - Required change: Query the apply button by `Apply for Principal Product Manager`.
      - Verification: Test posts the real job action and shows the next-step message.
      - Coverage category: Regression case
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/mock_jobs.spec.ts` all tests using `openMockJobs`
      - Required change: Fix the entry helper so it waits for the calibration deck state required by the plans.
      - Verification: `npx playwright test e2e/mock_jobs.spec.ts` passes.
      - Coverage category: Regression case
    - `/Users/devuser/dev/personal/recruiter/zoracrew-ui-host/zoracrew-ui/e2e/real_jobs.spec.ts` failed plan-required tests
      - Required change: Fix calibration helper, alert scoping, and apply request URL expectation.
      - Verification: `npx playwright test e2e/real_jobs.spec.ts` passes.
      - Coverage category: Regression case
- **Resource files needing changes:**
  - None
- **Notes of major removals:**
  - None

## 13. Summary

- Percent complete: 74%
- Rationale: Search status/results/no-results/retry/reconnect/job-card behavior is mostly implemented and covered by passing component tests. The combined plan is not yet complete because calibration is not implemented through the plan-owned `ChatShell` path, real-search start omits the required search-start API call, and required browser verification for mock and real job flows is failing.
