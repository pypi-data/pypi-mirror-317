// SPDX-License-Identifier: GPL-3.0-or-later
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

pragma solidity >=0.7.0 <0.9.0;

import "./ISilo.sol";

interface IShareToken {
    /**
     * @dev returns the underlying asset
     */
    function asset() external view returns (address);

    /**
     * @dev returns the address of the silo
     */
    function silo() external view returns (ISilo);

    /**
     * @dev returns the supply of the shareToken
     */
    function totalSupply() external view returns (uint256);
}
