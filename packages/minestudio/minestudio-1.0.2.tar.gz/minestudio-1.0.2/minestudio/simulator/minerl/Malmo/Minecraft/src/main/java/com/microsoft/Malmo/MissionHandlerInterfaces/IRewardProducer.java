// --------------------------------------------------------------------------------------------------
//  Copyright (c) 2016 Microsoft Corporation
//  
//  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
//  associated documentation files (the "Software"), to deal in the Software without restriction,
//  including without limitation the rights to use, copy, modify, merge, publish, distribute,
//  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//  
//  The above copyright notice and this permission notice shall be included in all copies or
//  substantial portions of the Software.
//  
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
//  NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
//  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// --------------------------------------------------------------------------------------------------

package com.microsoft.Malmo.MissionHandlerInterfaces;

import com.microsoft.Malmo.MissionHandlers.MultidimensionalReward;
import com.microsoft.Malmo.Schemas.MissionInit;

/**
 * Interface for objects which are responsible for providing a reward signal for
 * reinforcement learning.<br>
 */
public interface IRewardProducer {

    /**
     * Get the reward value for the current Minecraft state.
     * 
     * @param missionInit
     *            the MissionInit object for the currently running mission,
     *            which may contain parameters for the reward requirements.
     * @param reward
     *            the reward structure being constructed.
     */
    public void getReward(MissionInit missionInit, MultidimensionalReward reward);

    /**
     * Called once before the mission starts - use for any necessary
     * initialisation.
     */
    public void prepare(MissionInit missionInit);

    /** Called once after the mission ends - use for any necessary cleanup. */
    public void cleanup();
}
